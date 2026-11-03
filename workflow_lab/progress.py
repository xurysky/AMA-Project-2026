"""Read-model only. Durable owns execution; blobs are bounded UI projections."""
import asyncio,json,os
from datetime import datetime,timezone
from functools import lru_cache
from azure.storage.blob import BlobServiceClient,ContentSettings
from azure.core.exceptions import ResourceExistsError,ResourceNotFoundError


def now():return datetime.now(timezone.utc).isoformat()
@lru_cache
def container():
    c=BlobServiceClient.from_connection_string(os.environ['AzureWebJobsStorage']).get_container_client('ama-workflow-runs')
    try:c.create_container()
    except ResourceExistsError:pass
    return c

def put(name,data,overwrite=True):
    container().upload_blob(name,json.dumps(data,ensure_ascii=False),overwrite=overwrite,content_settings=ContentSettings(content_type='application/json'))

def get(name):
    return json.loads(container().download_blob(name).readall())

def node(run_id,node_id,status,*,input_data=None,output=None,mode='rules',error=None):
    key=f'{run_id}/nodes/{node_id}.json'
    try:previous=get(key)
    except ResourceNotFoundError:previous={}
    t=now();d={**previous,'id':node_id,'status':status,'mode':mode,'updated_at':t}
    if status=='running':d['started_at']=previous.get('started_at',t)
    if status in ['completed','failed','rejected','skipped']:d['finished_at']=t
    if input_data is not None:d['input']=input_data
    if output is not None:d['output']=output
    if error:d['error']=error
    put(key,d)
    return d

async def record(*args,**kwargs):await asyncio.to_thread(node,*args,**kwargs)

def list_nodes(run_id):
    return [json.loads(container().download_blob(x.name).readall()) for x in container().list_blobs(name_starts_with=run_id+'/nodes/')]
