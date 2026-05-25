from dotenv import load_dotenv
load_dotenv()
"""Azure OpenAI + Cosmos DB integration for AMA Agent Platform."""
import os
import json

try:
    from openai import AzureOpenAI
except Exception:  # optional for offline/mock demo mode
    AzureOpenAI = None

try:
    from azure.cosmos import CosmosClient
except Exception:  # optional for offline/mock demo mode
    CosmosClient = None

# ── Azure OpenAI ──
_openai_client = None
def get_openai():
    global _openai_client
    if AzureOpenAI is None:
        raise RuntimeError("openai package is not installed; running in offline mock mode")
    if _openai_client is None:
        _openai_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://japaneast.api.cognitive.microsoft.com/"),
            api_key=os.getenv("AZURE_OPENAI_KEY") or os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version="2024-12-01-preview",
        )
    return _openai_client

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

def call_gpt(system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> str:
    """Call Azure OpenAI GPT-4o and return the response text."""
    try:
        client = get_openai()
        resp = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_completion_tokens=max_tokens,
            temperature=0.3,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[Azure OpenAI call failed: {e}]"

def call_gpt_json(system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> dict:
    """Call Azure OpenAI and parse JSON response."""
    text = call_gpt(system_prompt, user_prompt, max_tokens)
    try:
        # Try to extract JSON from the response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        return {"raw_response": text}

# ── Cosmos DB ──
_cosmos_client = None
_cosmos_containers = {}

def get_cosmos(container_name: str = None):
    global _cosmos_client, _cosmos_containers
    if CosmosClient is None:
        raise RuntimeError("azure-cosmos package is not installed; running in offline mock mode")
    container_name = container_name or os.getenv("AZURE_COSMOS_CONTAINER", "customer360")
    if container_name not in _cosmos_containers:
        _cosmos_client = CosmosClient(
            os.getenv("AZURE_COSMOS_ENDPOINT", "https://ama-cosmos.documents.azure.com:443/"),
            os.getenv("AZURE_COSMOS_KEY", ""),
        )
        db = _cosmos_client.get_database_client(os.getenv("AZURE_COSMOS_DB", "ama-retail"))
        _cosmos_containers[container_name] = db.get_container_client(container_name)
    return _cosmos_containers[container_name]

def upsert_customer(customer_data: dict) -> dict:
    """Upsert a customer profile to Cosmos DB."""
    try:
        container = get_cosmos()
        container.upsert_item(customer_data)
        return {"status": "ok", "store": "cosmos_db"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def query_customers(filter_expr: str = None, max_items: int = 10) -> list:
    """Query customer profiles from Cosmos DB."""
    try:
        container = get_cosmos()
        query = "SELECT * FROM c"
        if filter_expr:
            query += f" WHERE {filter_expr}"
        items = list(container.query_items(query=query, max_item_count=max_items))
        return items
    except Exception as e:
        return [{"error": str(e)}]

# ── Stateful run store ──
RUN_STORE_ENABLED = os.getenv("ENABLE_COSMOS_RUN_STORE", "false").lower() == "true"
RUNS_CONTAINER = os.getenv("AZURE_COSMOS_RUNS_CONTAINER", "agentRuns")

def run_store_enabled() -> bool:
    """Return whether stateful run persistence should use Cosmos DB."""
    return RUN_STORE_ENABLED

def upsert_run(run: dict) -> dict:
    """Persist a run/work-order state document to Cosmos DB when enabled."""
    if not RUN_STORE_ENABLED:
        return {"status": "skipped", "store": "memory"}
    try:
        container = get_cosmos(RUNS_CONTAINER)
        item = dict(run)
        item["id"] = item["run_id"]
        item["partition_key"] = item.get("region", "global")
        container.upsert_item(item)
        return {"status": "ok", "store": "cosmos_db", "container": RUNS_CONTAINER}
    except Exception as e:
        return {"status": "error", "detail": str(e), "container": RUNS_CONTAINER}

def read_run(run_id: str, region: str = None) -> dict | None:
    """Read a run from Cosmos DB. Falls back to a cross-partition query when region is unknown."""
    if not RUN_STORE_ENABLED:
        return None
    try:
        container = get_cosmos(RUNS_CONTAINER)
        if region:
            return container.read_item(item=run_id, partition_key=region)
        query = "SELECT * FROM c WHERE c.run_id = @run_id"
        params = [{"name": "@run_id", "value": run_id}]
        rows = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
        return rows[0] if rows else None
    except Exception:
        return None

# ── Agent Decision with GPT-4o ──
def agent_decide(agent_name: str, context: str, task: str) -> dict:
    """Have GPT-4o make an agent decision."""
    # Detect if this is a creative/content generation task
    is_creative = any(kw in task.lower() for kw in ['generate', 'subject line', 'push', 'copy', 'script', 'message', 'banner', 'talking point', 'recommend', '文案', '推送', '话术', '生成'])
    
    if is_creative:
        system = f"""You are {agent_name} in an Autonomous Retail Intelligence Platform.
Your job is to generate creative content based on the context.
Generate the actual content directly. Do not summarize or describe what you would generate - actually generate it.
Be specific, actionable, and ready to use."""
        user = f"""Context: {context}

Task: {task}

Generate the actual content now. Be specific and direct."""
        result = call_gpt(system, user, max_tokens=800)
        return {"decision": result, "confidence": 0.92}
    else:
        system = f"""You are {agent_name} in an Autonomous Retail Intelligence Platform.
Your job is to analyze the given context and make a decision.

Respond in JSON format with these fields:
- "decision": your decision summary
- "reasoning": brief reasoning
- "confidence": 0.0-1.0
- "actions": list of recommended actions
- "risks": list of potential risks"""
        
        user = f"""Context: {context}

Task: {task}

Respond with JSON only."""
        
        return call_gpt_json(system, user)

def orchestrator_decompose(business_event: str, season: str, region: str) -> dict:
    """Have GPT-4o decompose a business event into agent tasks."""
    system = """You are the Orchestrator Agent (Agent Orchestrator) in a retail AI platform.
Decompose the business event into sub-tasks for 5 specialist agents.

Respond in JSON:
{
  "summary": "one-line summary",
  "sub_tasks": [
    {"agent": "Inventory Agent", "task": "...", "priority": "high/medium/low"},
    {"agent": "Pricing Agent", "task": "...", "priority": "..."},
    {"agent": "Customer Understanding Agent", "task": "...", "priority": "..."},
    {"agent": "Personalization Agent", "task": "...", "priority": "..."},
    {"agent": "Marketing Agent", "task": "...", "priority": "..."}
  ],
  "risk_assessment": "...",
  "estimated_impact": "..."
}"""
    
    user = f"""Business Event: {business_event}
Season: {season}
Region: {region}

Decompose this into agent tasks. Respond with JSON only."""
    
    return call_gpt_json(system, user)
