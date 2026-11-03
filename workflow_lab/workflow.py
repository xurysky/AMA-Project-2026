"""A bounded, typed MAF graph checkpointed by the official Durable Extension.
All stock, audience and policy facts in this pilot are synthetic demo inputs.
"""
from __future__ import annotations
import asyncio,copy,hashlib,json,os
from datetime import datetime,timezone
from agent_framework import Executor,WorkflowBuilder,WorkflowContext,executor,handler,response_handler
from pydantic import BaseModel,ConfigDict
from typing_extensions import Never
from progress import record,now,put,get


def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

@executor(id='snapshot')
async def snapshot(data:dict,ctx:WorkflowContext[dict])->None:
    r=data['run_id'];await record(r,'snapshot','running',input_data={'case_id':data['case']['case_id'],'version':data['snapshot_hash']})
    # Verify immutable server-selected input, never accept arbitrary objects or prompts.
    assert digest(data['case'])==data['snapshot_hash']
    await record(r,'snapshot','completed',output={'case_id':data['case']['case_id'],'data_kind':'synthetic_demo','snapshot_hash':data['snapshot_hash']})
    await ctx.send_message(data)

@executor(id='inventory')
async def inventory(data:dict,ctx:WorkflowContext[dict])->None:
    d=copy.deepcopy(data);i=d['case']['inventory'];r=d['run_id']
    await record(r,'inventory','running',input_data={k:i[k] for k in ['physical_on_hand','soft_reserved','safety_stock','blocked_or_quarantined','returned_pending_inspection']})
    atp=max(0,i['physical_on_hand']-i['soft_reserved']-i['safety_stock']-i['blocked_or_quarantined'])
    d['inventory_result']={'sellable_atp':atp,'transfer_qty':min(320,atp),'days_of_supply':round(atp/i['demand_units_per_day'],1),'excluded_returns':i['returned_pending_inspection'],'evidence':['POS','Returns','Store Task']}
    await record(r,'inventory','completed',output=d['inventory_result']);await ctx.send_message(d)

@executor(id='pricing')
async def pricing(data:dict,ctx:WorkflowContext[dict])->None:
    d=copy.deepcopy(data);v=d['case']['variant'];r=d['run_id'];await record(r,'pricing','running',input_data={'atp':d['inventory_result']['sellable_atp'],'price':v['current_price_cny'],'unit_cost':v['unit_cost_cny'],'margin_floor':v['margin_floor_pct'],'pilot_discount_cap':20})
    price=round(v['current_price_cny']*.85,2);margin=round((price-v['unit_cost_cny'])/price*100,2)
    d['pricing_result']={'discount_pct':15,'unit_price':price,'gross_margin_pct':margin,'margin_floor_pct':v['margin_floor_pct'],'discount_cap_pct':20,'rejected_discount_pct':30,'rejection_reason':'超过试用策略20%折扣上限，不是按当前数字计算的毛利不足','eligible':margin>=v['margin_floor_pct'],'policy_version':'pilot-discount-cap-20-v1'}
    await record(r,'pricing','completed',output=d['pricing_result']);d['branch']='supply';await ctx.send_message(d)

@executor(id='customer')
async def customer(data:dict,ctx:WorkflowContext[dict])->None:
    d=copy.deepcopy(data);r=d['run_id'];await record(r,'customer','running',input_data={'audience_source':'synthetic aggregates','policy':'prior marketing consent required'})
    # A fixed input fixture, not invented live customer inference.
    audience=d['demo_audience'];eligible=sum(x['count'] for x in audience if x['consented'] and x['recent_outerwear_intent'])
    d['customer_result']={'eligible_members':eligible,'excluded_members':sum(x['count'] for x in audience)-eligible,'consent_required':True,'source':'虚构分组数据；无个人资料'}
    await record(r,'customer','completed',output=d['customer_result']);await ctx.send_message(d)

@executor(id='personalization')
async def personalization(data:dict,ctx:WorkflowContext[dict])->None:
    d=copy.deepcopy(data);r=d['run_id'];await record(r,'personalization','running',input_data=d['customer_result'])
    d['personalization_result']={'audience_count':d['customer_result']['eligible_members'],'variant':d['case']['variant']['variant_id'],'channel':'member-app-draft','requires_atp_recheck':True,'content_scope':'仅生成会员优惠草稿，不发送'}
    await record(r,'personalization','completed',output=d['personalization_result']);d['branch']='audience';await ctx.send_message(d)

@executor(id='proposal')
async def proposal(parts:list[dict],ctx:WorkflowContext[dict])->None:
    supply=next(x for x in parts if x['branch']=='supply');aud=next(x for x in parts if x['branch']=='audience');d=copy.deepcopy(supply)
    assert supply['snapshot_hash']==aud['snapshot_hash']
    d.update({k:aud[k] for k in ['customer_result','personalization_result']});r=d['run_id'];mode='model' if d['use_model'] else 'rules'
    await record(r,'proposal','running',input_data={'inventory':d['inventory_result'],'pricing':d['pricing_result'],'audience':d['customer_result']},mode=mode)
    facts={'transfer_qty':d['inventory_result']['transfer_qty'],'discount_pct':15,'eligible_members':d['customer_result']['eligible_members'],'blocked_discount_pct':30,'approval_required':True}
    if d['use_model']:
        try:
            from agent_framework import Agent
            from agent_framework.openai import OpenAIChatClient
            client=OpenAIChatClient(azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],model=os.environ['AZURE_OPENAI_DEPLOYMENT'],api_version=os.environ.get('AZURE_OPENAI_API_VERSION','preview'),api_key=os.environ['AZURE_OPENAI_KEY'])
            client.client.max_retries=0
            agent=Agent(client=client,name='MarketingProposal',instructions='你是零售方案摘要助手。仅用给定虚构事实，以中文写三条简短建议。不可修改数字、声称已执行或编造收益。说明30%折扣因超过试用策略20%上限被拦截。不要输出隐藏推理过程。')
            result=await asyncio.wait_for(agent.run(json.dumps(facts,ensure_ascii=False),options={'max_tokens':800,'reasoning':{'effort':'low'},'store':False}),timeout=75)
            text=result.text
            if not text:raise ValueError('Empty model response')
            usage=getattr(result,'usage_details',None);usage=usage.to_dict() if hasattr(usage,'to_dict') else dict(usage or {})
            summary={'text':text,'model':os.environ['AZURE_OPENAI_DEPLOYMENT'],'usage':usage,'model_calls':1}
        except Exception:
            await record(r,'proposal','failed',error='模型摘要未完成。没有生成可审批方案，请查看运行详情后重试。',mode=mode)
            raise RuntimeError('Model summary failed; no fallback presented as model output') from None
    else:summary={'text':'先调拨320件缓解积压；准备15%会员优惠草稿；仅面向已授权人群，审批后才进入演示执行。','model_calls':0,'usage':{},'model':None}
    d['proposal']={**facts,**summary};d['proposal_hash']=digest({'facts':facts,'snapshot':d['snapshot_hash'],'policy':d['pricing_result']['policy_version']})
    await record(r,'proposal','completed',output=d['proposal'],mode=mode);await ctx.send_message(d)

@executor(id='policy')
async def policy(data:dict,ctx:WorkflowContext[dict])->None:
    d=copy.deepcopy(data);r=d['run_id'];await record(r,'policy','running',input_data={'snapshot_hash':d['snapshot_hash'],'proposal_hash':d['proposal_hash']})
    assert d['pricing_result']['eligible'] and d['customer_result']['consent_required']
    assert d['inventory_result']['transfer_qty']<=d['inventory_result']['sellable_atp']
    assert d['pricing_result']['discount_pct']<=d['pricing_result']['discount_cap_pct']
    await record(r,'policy','completed',output={'result':'通过','blocked_option':'30%折扣超过20%试用上限','execution_scope':'仅演示回执，不写生产系统'})
    await ctx.send_message(d)

class Decision(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    approved:bool
    proposal_hash:str
    actor:str

class Approval(Executor):
    @handler
    async def ask(self,data:dict,ctx:WorkflowContext[dict])->None:
        await record(data['run_id'],'approval','waiting',input_data={'proposal':data['proposal'],'proposal_hash':data['proposal_hash'],'expires_at':data['expires_at'],'role':'试用审核者（不代表生产审批权）'})
        await ctx.request_info(request_data=data,response_type=object)
    @response_handler
    async def resume(self,original_request:dict,response:object,ctx:WorkflowContext[dict])->None:
        # Azure-managed Durable event transports may return JSON text while the
        # local runner returns a mapping. Normalize exactly one JSON layer, then
        # enforce the same strict domain contract (never deserialize Python types).
        wire_type=type(response).__name__
        if isinstance(response,str):response=json.loads(response)
        response=Decision.model_validate(response)
        d=copy.deepcopy(original_request)
        if response.proposal_hash!=d['proposal_hash']:raise ValueError('Approval does not match proposal')
        if datetime.now(timezone.utc)>datetime.fromisoformat(d['expires_at']):raise ValueError('Proposal expired')
        d['approved']=response.approved;d['approved_by']=response.actor
        await record(d['run_id'],'approval','completed' if response.approved else 'rejected',output={'approved':response.approved,'actor':response.actor,'scope':'演示审批','transport_type':wire_type})
        await ctx.send_message(d)

@executor(id='receipt')
async def receipt(data:dict,ctx:WorkflowContext[Never,dict])->None:
    d=data;r=d['run_id']
    if not d['approved']:
        out={'status':'rejected','message':'方案已拒绝，未执行任何业务动作'};await record(r,'receipt','skipped',output=out);await ctx.yield_output(out);return
    await record(r,'receipt','running',input_data={'proposal_hash':d['proposal_hash'],'snapshot_hash':d['snapshot_hash']})
    assert digest(d['case'])==d['snapshot_hash']
    key=f'{r}/receipt.json'
    out={'status':'completed','scope':'demo_only','idempotency_key':r+':'+d['proposal_hash'],'transfer_request':{'quantity':d['proposal']['transfer_qty'],'status':'DEMO_RECEIPT'},'member_voucher':{'discount_pct':15,'status':'DRAFT_ONLY'},'business_actions_sent':0,'finished_at':now()}
    from azure.core.exceptions import ResourceExistsError
    try:await asyncio.to_thread(put,key,out,False)
    except ResourceExistsError:out=await asyncio.to_thread(get,key)
    await record(r,'receipt','completed',output=out);await ctx.yield_output(out)

approval=Approval(id='approval')
def build_workflow():
    return (WorkflowBuilder(name='ama_retail_pilot',start_executor=snapshot,max_iterations=16)
      .add_fan_out_edges(snapshot,[inventory,customer])
      .add_edge(inventory,pricing).add_edge(customer,personalization)
      .add_fan_in_edges([pricing,personalization],proposal)
      .add_edge(proposal,policy).add_edge(policy,approval).add_edge(approval,receipt).build())
