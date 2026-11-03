"""Gateway-only pilot endpoints. Function keys never enter the browser.
The existing Entra-protected demo gateway overwrites the principal header.
"""
from __future__ import annotations
import asyncio,hashlib,json,os,re,uuid
from datetime import datetime,timedelta,timezone
from pathlib import Path
import azure.functions as func
import azure.durable_functions as df
from agent_framework_azurefunctions import AgentFunctionApp
from azure.core.exceptions import ResourceExistsError,ResourceNotFoundError
from workflow import build_workflow,digest
from progress import container,get,put,list_nodes,now

app=AgentFunctionApp(workflow=build_workflow(),enable_http_endpoints=False,enable_health_check=False,http_auth_level=func.AuthLevel.FUNCTION)
HERE=Path(__file__).parent
NODE_IDS=['snapshot','inventory','customer','pricing','personalization','proposal','policy','approval','receipt']

def response(data,status=200):
    return func.HttpResponse(json.dumps(data,ensure_ascii=False),status_code=status,mimetype='application/json',headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'})

def principal(req):
    oid=req.headers.get('x-ms-client-principal-id','')
    if oid not in os.environ.get('PILOT_ALLOWED_PRINCIPALS','').split(','):raise PermissionError('Authenticated pilot access required')
    return oid

def authorize_run(req,run_id):
    oid=principal(req)
    if not re.fullmatch(r'ama-[0-9a-f]{32}',run_id):raise ResourceNotFoundError('Run not found')
    meta=get(f'{run_id}/meta.json')
    if meta['owner']!=oid:raise PermissionError('Run not available')
    return oid,meta

def pending(status):
    c=status.custom_status or {}
    if not isinstance(c,dict):return []
    return [{'request_id':k,'executor':v.get('source_executor_id')} for k,v in c.get('pending_requests',{}).items()]

@app.route(route='lab/health',methods=['GET'])
def health(req:func.HttpRequest):
    from importlib.metadata import version
    return response({'ok':True,'workflow':'ama_retail_pilot','data_kind':'synthetic_demo','framework':version('agent-framework-core'),'durable_extension':version('agent-framework-azurefunctions'),'backend':'durable-task-scheduler-consumption'})

@app.route(route='lab/{asset?}',methods=['GET'])
def static(req:func.HttpRequest):
    try:principal(req)
    except PermissionError:return response({'error':'请通过演示平台登录后访问'},403)
    name=req.route_params.get('asset') or 'index.html'
    if name not in ['index.html','app.js','style.css']:return response({'error':'Not found'},404)
    mime={'index.html':'text/html','app.js':'application/javascript','style.css':'text/css'}[name]
    return func.HttpResponse((HERE/'ui'/name).read_bytes(),mimetype=mime,headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'self'; base-uri 'self'; form-action 'self'"})

@app.route(route='lab/runs',methods=['POST'])
@app.durable_client_input(client_name='client')
async def start(req:func.HttpRequest,client:df.DurableOrchestrationClient):
    try:
        oid=principal(req);body=req.get_json()
        if not isinstance(body,dict) or set(body)-{'request_id','use_model'}:return response({'error':'无效请求'},400)
        request_id=str(uuid.UUID(body['request_id']));use_model=body.get('use_model',False)
        if not isinstance(use_model,bool):return response({'error':'use_model必须是布尔值'},400)
    except PermissionError:return response({'error':'未获试用授权'},403)
    except (ValueError,KeyError,TypeError):return response({'error':'请提供有效请求标识'},400)
    # Stable owner-bound ID; one create wins. No browser-controlled workflow, facts, or prompt.
    rid='ama-'+hashlib.sha256((oid+request_id).encode()).hexdigest()[:32];meta_key=rid+'/meta.json'
    try:
        old=await asyncio.to_thread(get,meta_key)
        if old['use_model']!=use_model:return response({'error':'同一请求不能修改模型选项'},409)
        existing=await client.get_status(rid)
        if existing:return response({'run_id':rid,'existing':True},202)
    except ResourceNotFoundError:pass
    # Small pilot quota; this is an application limit, not an Azure billing cap.
    owner_hash=hashlib.sha256(oid.encode()).hexdigest()[:20];today=datetime.now(timezone.utc).date().isoformat()
    prefix=f'quota/{owner_hash}/{today}/'
    count=await asyncio.to_thread(lambda:sum(1 for _ in container().list_blobs(name_starts_with=prefix)))
    if count>=20:return response({'error':'今日试用次数已达20次上限'},429)
    # Only one active run per allowed owner. Lease prevents concurrent double submissions.
    lock_blob=container().get_blob_client(f'locks/{owner_hash}')
    try:await asyncio.to_thread(lock_blob.upload_blob,'{}',overwrite=False)
    except ResourceExistsError:pass
    try:lease=await asyncio.to_thread(lock_blob.acquire_lease,lease_duration=15)
    except Exception:return response({'error':'另一项操作正在提交，请稍后重试'},409)
    try:
        previous=json.loads(await asyncio.to_thread(lambda:lock_blob.download_blob(lease=lease).readall()))
        existing=await client.get_status(rid)
        if existing:return response({'run_id':rid,'existing':True},202)
        if previous.get('run_id'):
            state=await client.get_status(previous['run_id'])
            if state and state.runtime_status in [df.OrchestrationRuntimeStatus.Running,df.OrchestrationRuntimeStatus.Pending,df.OrchestrationRuntimeStatus.Suspended]:return response({'error':'已有运行尚未结束，请先处理审批或结束它','run_id':previous['run_id']},409)
        case=json.loads((HERE/'sample_case.json').read_text())['case'];created=now();expires=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()
        data={'run_id':rid,'case':case,'snapshot_hash':digest(case),'use_model':use_model,'demo_audience':[{'count':280,'consented':True,'recent_outerwear_intent':True},{'count':90,'consented':False,'recent_outerwear_intent':True},{'count':130,'consented':True,'recent_outerwear_intent':False}],'expires_at':expires}
        meta={'run_id':rid,'owner':oid,'created_at':created,'expires_at':expires,'use_model':use_model,'case_id':case['case_id'],'workflow_version':'1.0.0','snapshot_hash':data['snapshot_hash'],'data_kind':'synthetic_demo'}
        try:await asyncio.to_thread(put,meta_key,meta,False)
        except ResourceExistsError:
            # A prior HTTP request may have persisted input before dispatch failed.
            # The owner lease and stable ID permit safe retry of the same submission.
            previous_meta=await asyncio.to_thread(get,meta_key)
            data['expires_at']=previous_meta['expires_at']
            if previous_meta['snapshot_hash']!=data['snapshot_hash']:return response({'error':'案例快照已变化，请新建运行'},409)
        await client.start_new('dafx-ama_retail_pilot',instance_id=rid,client_input=data)
        await asyncio.to_thread(put,prefix+rid,{'created_at':created},False)
        await asyncio.to_thread(lock_blob.upload_blob,json.dumps({'run_id':rid}),overwrite=True,lease=lease)
        return response({'run_id':rid,'existing':False},202)
    finally:await asyncio.to_thread(lease.release)

@app.route(route='lab/runs/{run_id}',methods=['GET'])
@app.durable_client_input(client_name='client')
async def status(req:func.HttpRequest,client:df.DurableOrchestrationClient):
    rid=req.route_params['run_id']
    try:oid,meta=await asyncio.to_thread(authorize_run,req,rid)
    except PermissionError:return response({'error':'未获授权'},403)
    except ResourceNotFoundError:return response({'error':'运行不存在'},404)
    s=await client.get_status(rid)
    if not s:return response({'run_id':rid,'status':'Pending','nodes':[],'meta':{k:v for k,v in meta.items() if k!='owner'},'pending':[]})
    nodes=await asyncio.to_thread(list_nodes,rid)
    return response({'run_id':rid,'status':s.runtime_status.name,'nodes':nodes,'pending':pending(s),'meta':{k:v for k,v in meta.items() if k!='owner'},'error':'运行未完成，请查看失败节点。没有执行生产业务动作。' if s.runtime_status==df.OrchestrationRuntimeStatus.Failed else None,'last_updated':s.last_updated_time.isoformat() if s.last_updated_time else None})

@app.route(route='lab/runs/{run_id}/decision',methods=['POST'])
@app.durable_client_input(client_name='client')
async def decision(req:func.HttpRequest,client:df.DurableOrchestrationClient):
    rid=req.route_params['run_id']
    try:
        oid,meta=await asyncio.to_thread(authorize_run,req,rid);body=req.get_json()
        if not isinstance(body,dict) or set(body)!={'approved','proposal_hash'} or not isinstance(body['approved'],bool):return response({'error':'无效审批请求'},400)
    except PermissionError:return response({'error':'未获授权'},403)
    except ResourceNotFoundError:return response({'error':'运行不存在'},404)
    except (ValueError,TypeError):return response({'error':'无效审批请求'},400)
    s=await client.get_status(rid)
    if not s or s.name!='dafx-ama_retail_pilot':return response({'error':'运行不存在'},404)
    try:proposal=await asyncio.to_thread(get,f'{rid}/nodes/approval.json')
    except ResourceNotFoundError:return response({'error':'尚未进入审批'},409)
    if proposal['input']['proposal_hash']!=body['proposal_hash']:return response({'error':'方案版本已变化，请刷新'},409)
    if datetime.now(timezone.utc)>datetime.fromisoformat(meta['expires_at']):return response({'error':'方案已过期，请结束本次运行后重新评估'},409)
    key=f'{rid}/decision.json'
    try:
        prior=await asyncio.to_thread(get,key)
        if prior['approved']!=body['approved']:return response({'error':'已有不同审批结果，不能覆盖'},409)
        requests=pending(s)
        if requests:await client.raise_event(rid,requests[0]['request_id'],prior)
        return response({'ok':True,'duplicate':True})
    except ResourceNotFoundError:pass
    requests=pending(s)
    if len(requests)!=1:return response({'error':'当前没有待处理审批'},409)
    payload={'approved':body['approved'],'proposal_hash':body['proposal_hash'],'actor':oid}
    try:await asyncio.to_thread(put,key,payload,False)
    except ResourceExistsError:return response({'error':'审批正在处理，请刷新'},409)
    await client.raise_event(rid,requests[0]['request_id'],payload)
    return response({'ok':True})

@app.route(route='lab/runs/{run_id}/stop',methods=['POST'])
@app.durable_client_input(client_name='client')
async def stop(req:func.HttpRequest,client:df.DurableOrchestrationClient):
    rid=req.route_params['run_id']
    try:await asyncio.to_thread(authorize_run,req,rid)
    except PermissionError:return response({'error':'未获授权'},403)
    except ResourceNotFoundError:return response({'error':'运行不存在'},404)
    s=await client.get_status(rid)
    if not s:return response({'error':'运行不存在'},404)
    if s.runtime_status in [df.OrchestrationRuntimeStatus.Completed,df.OrchestrationRuntimeStatus.Failed,df.OrchestrationRuntimeStatus.Terminated]:return response({'ok':True,'unchanged':True})
    await client.terminate(rid,'Pilot user ended the run. No production actions exist.')
    return response({'ok':True})
