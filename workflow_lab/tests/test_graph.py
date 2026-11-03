import sys,json,asyncio,copy
from pathlib import Path
from datetime import datetime,timezone,timedelta
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import workflow as w
from azure.core.exceptions import ResourceExistsError
records={};receipts={}
async def record(run,node,status,**kw):records[node]={'status':status,**kw}
def put(k,v,overwrite=True):
 if k in receipts and not overwrite:raise ResourceExistsError('exists')
 receipts[k]=copy.deepcopy(v)
def get(k):return copy.deepcopy(receipts[k])
w.record=record;w.put=put;w.get=get
case=json.loads((Path(__file__).resolve().parents[1]/'sample_case.json').read_text())['case']
base={'run_id':'test','case':case,'snapshot_hash':w.digest(case),'use_model':False,'demo_audience':[{'count':280,'consented':True,'recent_outerwear_intent':True},{'count':90,'consented':False,'recent_outerwear_intent':True},{'count':130,'consented':True,'recent_outerwear_intent':False}],'expires_at':(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()}
async def test(approved,transport="mapping"):
 graph=w.build_workflow();events=await graph.run(copy.deepcopy(base));requests=[e for e in events if e.type=='request_info'];assert len(requests)==1
 assert records['inventory']['output']['sellable_atp']==1000
 assert records['customer']['output']['eligible_members']==280
 assert records['pricing']['output']['gross_margin_pct']>38
 assert records['pricing']['output']['discount_cap_pct']==20
 assert records['approval']['status']=='waiting'
 request=requests[0];print('request attrs',request.request_id)
 reply={'approved':approved,'proposal_hash':records['approval']['input_data']['proposal_hash'],'actor':'test'}
 if transport=='json':reply=json.dumps(reply)
 result=await graph.run(responses={request.request_id:reply})
 out=[e.data for e in result if e.type=='output'];assert out
 assert out[-1]['status']==('completed' if approved else 'rejected')
 print('PASS',transport,('approve' if approved else 'reject'),out[-1]['status'])
for transport in ['mapping','json']:
 for approved in [True,False]:
  receipts.clear();records.clear();asyncio.run(test(approved,transport))
