# Agent Collaboration Patterns

## Overview

The 5 agents in the Autonomous Retail Intelligence Platform collaborate through well-defined patterns inspired by real-world retail operations. This document details the three core collaboration mechanisms: **Handoff**, **Reflection**, and **State Graph**.

---

## 1. Handoff Pattern (Task Delegation)

Handoff is the primary collaboration mechanism where one agent delegates a task to another agent and receives the result.

### Flow
```
Agent A (Requester)                    Agent B (Executor)
       │                                      │
       │── handoff_request ──────────────────→ │
       │   {task, context, priority}           │
       │                                      │
       │                                      │── process task
       │                                      │
       │ ←──────────────────── handoff_result ─│
       │   {result, confidence, metadata}      │
       │                                      │
       │── continue workflow                   │
```

### Example 1: Inventory → Pricing Handoff (Overstock Response)

```python
# Inventory Agent detects overstock
async def handle_overstock(self, sku_id: str, store_id: str):
    """When inventory is too high, hand off to Pricing Agent for discount strategy"""
    
    handoff_request = AgentMessage(
        sender="inventory-agent",
        receiver="pricing-agent",
        message_type="handoff_request",
        content={
            "task": "generate_discount_strategy",
            "context": {
                "sku_id": sku_id,
                "store_id": store_id,
                "current_stock": 450,
                "target_stock": 200,
                "days_to_clear": 14,
                "category": "outerwear"
            },
            "priority": "high",
            "constraints": {
                "min_discount": 10,
                "max_discount": 40,
                "preserve_brand_value": True
            }
        }
    )
    
    result = await self.send_and_wait(handoff_request)
    
    # Pricing Agent returns discount strategy
    return {
        "action": "apply_discount",
        "discount_pct": result["recommended_discount"],
        "duration_days": result["campaign_duration"],
        "channels": result["recommended_channels"],
        "expected_clear_rate": result["predicted_clear_rate"]
    }
```

### Example 2: Customer Understanding → Personalization Handoff

```python
# Customer Understanding Agent builds profile, hands off to Personalization
async def process_customer_event(self, event: Dict):
    """Build customer profile then hand off for personalized recommendations"""
    
    # Step 1: Build unified profile
    profile = await self._build_unified_profile(event)
    
    # Step 2: Hand off to Personalization Agent
    handoff_request = AgentMessage(
        sender="customer-understanding-agent",
        receiver="personalization-agent",
        message_type="handoff_request",
        content={
            "task": "generate_recommendations",
            "context": {
                "customer_profile": profile,
                "current_channel": event["channel"],
                "session_context": event.get("session", {}),
                "inventory_snapshot": event.get("inventory", [])
            },
            "priority": "realtime",  # Customer is browsing NOW
            "constraints": {
                "max_recommendations": 8,
                "diversity_threshold": 0.3,
                "include_explanation": True
            }
        }
    )
    
    result = await self.send_and_wait(handoff_request, timeout_ms=500)
    
    return result
```

### Handoff Rules

| Rule | Description |
|------|-------------|
| **Timeout** | Handoff must complete within defined SLA (realtime: 500ms, batch: 30s) |
| **Fallback** | If handoff fails, use cached/default response |
| **Priority** | Critical handoffs (customer-facing) preempt batch handoffs |
| **Idempotency** | Same handoff request produces same result (within time window) |
| **Tracing** | Every handoff carries correlation_id for end-to-end tracing |

---

## 2. Reflection Pattern (Self-Improvement)

Reflection allows agents to evaluate their own decisions and improve over time.

### Flow
```
Agent makes decision
       │
       ▼
Execute decision
       │
       ▼
Observe outcome
       │
       ▼
Reflect: Was the outcome good?
       │
       ├── Yes → Reinforce strategy
       └── No  → Adjust parameters / escalate
```

### Example 1: Pricing Agent Reflection

```python
class PricingAgent(BaseAgent):
    """Dynamic pricing with reflection"""
    
    async def reflect_on_decision(self, decision_id: str, actual_outcome: Dict):
        """Reflect on a pricing decision after observing results"""
        
        # Get original decision
        original = await self._get_decision(decision_id)
        
        # Compare predicted vs actual
        predicted_revenue = original["predicted_revenue"]
        actual_revenue = actual_outcome["revenue"]
        accuracy = 1 - abs(predicted_revenue - actual_revenue) / predicted_revenue
        
        # Reflection prompt to LLM
        reflection = await self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a pricing strategy analyst. Analyze the pricing decision and suggest improvements."},
                {"role": "user", "content": f"""
                Original Decision:
                - SKU: {original['sku_id']}
                - Price change: {original['old_price']} → {original['new_price']}
                - Predicted revenue: {predicted_revenue}
                - Confidence: {original['confidence']}
                
                Actual Outcome:
                - Revenue: {actual_revenue}
                - Units sold: {actual_outcome['units']}
                - Customer complaints: {actual_outcome.get('complaints', 0)}
                
                Analysis Questions:
                1. Was the price change too aggressive or too conservative?
                2. Did the prediction model account for all factors?
                3. What should be adjusted for future decisions?
                """}
            ]
        )
        
        insights = reflection.choices[0].message.content
        
        # Store reflection for future decisions
        await self._store_reflection({
            "decision_id": decision_id,
            "accuracy": accuracy,
            "insights": insights,
            "adjustments": self._extract_adjustments(insights),
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # If accuracy < 70%, trigger model retraining
        if accuracy < 0.7:
            await self._trigger_model_retrain(original["sku_id"])
```

### Example 2: Marketing Agent Reflection (Campaign Effectiveness)

```python
async def reflect_on_campaign(self, campaign_id: str, results: Dict):
    """Evaluate campaign performance and extract learnings"""
    
    campaign = await self._get_campaign(campaign_id)
    
    reflection = await self.openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a marketing analytics expert."},
            {"role": "user", "content": f"""
            Campaign: {campaign['name']}
            Target segment: {campaign['segment']}
            Channels: {campaign['channels']}
            Budget: ¥{campaign['budget']}
            
            Results:
            - Impressions: {results['impressions']}
            - CTR: {results['ctr']}%
            - Conversions: {results['conversions']}
            - ROI: {results['roi']}x
            - Best channel: {results['best_channel']}
            
            What worked? What didn't? What should we change next time?
            """}
        ]
    )
    
    # Update campaign playbook
    await self._update_playbook({
        "segment": campaign["segment"],
        "what_worked": extract_positive_insights(reflection),
        "what_failed": extract_negative_insights(reflection),
        "recommended_changes": extract_recommendations(reflection)
    })
```

---

## 3. State Graph Pattern (Shared Context)

All agents share a real-time customer state graph that updates as interactions happen.

### State Graph Structure
```json
{
  "customer_id": "UNIQLO_2026_001",
  "state": {
    "current_session": {
      "channel": "app",
      "started_at": "2026-05-05T10:00:00Z",
      "pages_viewed": ["homepage", "outerwear", "product_4471"],
      "intent_signals": ["browsing_winter", "comparing_prices"]
    },
    "profile": {
      "segment": "young_professional",
      "lifetime_value": 12500,
      "price_sensitivity": "medium",
      "preferred_categories": ["basics", "outerwear"]
    },
    "active_recommendations": [
      {"sku": "4471", "agent": "personalization", "confidence": 0.92}
    ],
    "inventory_context": {
      "store": "SH-001",
      "nearby_stock": {"4471": 45, "3382": 12}
    },
    "pricing_context": {
      "active_promotions": ["winter_sale_20"],
      "price_alerts": []
    },
    "marketing_context": {
      "active_campaigns": ["spring_launch"],
      "last_contact": "2026-05-01",
      "contact_frequency": "weekly"
    }
  },
  "version": 42,
  "last_updated_by": "personalization-agent",
  "last_updated_at": "2026-05-05T10:02:15Z"
}
```

### State Update Protocol

```python
class StateGraph:
    """Shared customer state across all agents"""
    
    def __init__(self, cosmos_client):
        self.cosmos = cosmos_client
    
    async def read_state(self, customer_id: str) -> Dict:
        """Read current customer state (any agent)"""
        return await self.cosmos.read_document(
            container="customer_state",
            partition_key=customer_id,
            document_id=customer_id
        )
    
    async def update_state(self, customer_id: str, agent_id: str, 
                           updates: Dict, expected_version: int) -> bool:
        """Update customer state with optimistic concurrency"""
        
        # Read current state
        current = await self.read_state(customer_id)
        
        # Version check (prevent lost updates)
        if current["version"] != expected_version:
            raise ConflictError(f"Version mismatch: expected {expected_version}, got {current['version']}")
        
        # Apply updates
        current["state"].update(updates)
        current["version"] += 1
        current["last_updated_by"] = agent_id
        current["last_updated_at"] = datetime.utcnow().isoformat()
        
        # Write back with version check
        await self.cosmos.replace_document(
            container="customer_state",
            document=current,
            etag=current["_etag"]
        )
        
        return True
    
    async def watch_state(self, customer_id: str, callback):
        """Subscribe to state changes (for reactive agents)"""
        # Using Cosmos DB Change Feed
        async for change in self.cosmos.get_change_feed(
            container="customer_state",
            partition_key=customer_id
        ):
            await callback(change)
```

### Agent Reactions to State Changes

| State Change | Reactive Agent | Action |
|-------------|---------------|--------|
| Customer views product | Personalization Agent | Generate recommendations |
| Stock drops below threshold | Inventory Agent | Trigger reorder |
| Price change detected | Marketing Agent | Update campaign messaging |
| Customer complaint logged | Customer Understanding Agent | Adjust sentiment score |
| Campaign conversion | Marketing Agent | Update ROI, adjust budget |

---

## 4. Orchestration: The "Cold Snap" Scenario

All three patterns work together in the "Cold Snap" scenario:

```
1. TRIGGER: Shanghai temperature drops 10°C
   └── State Graph: Update weather_context.temperature = -5°C

2. REACTION (State Graph):
   ├── Inventory Agent: Demand spike predicted for warm clothing
   │   └── Handoff → Pricing Agent: "Adjust pricing for high-demand items"
   │       └── Pricing Agent: Recommend strategic pricing (not gouging)
   │
   ├── Marketing Agent: Launch "Stay Warm" campaign
   │   └── Handoff → Personalization Agent: "Get audience for warm clothing campaign"
   │       └── Personalization Agent: Return segmented customer list
   │
   └── Customer Understanding Agent: Update intent signals
       └── State Graph: Mark customers with "winter_shopping" intent

3. REFLECTION (after 24 hours):
   ├── Pricing Agent: Did pricing strategy maximize revenue without complaints?
   ├── Marketing Agent: What was campaign CTR and conversion?
   └── Inventory Agent: Was demand prediction accurate?
```

---

## Collaboration Matrix

| From → To | Pattern | Frequency | Latency SLA |
|-----------|---------|-----------|-------------|
| Customer Understanding → Personalization | Handoff | Real-time | 500ms |
| Customer Understanding → Marketing | State Graph | Near-realtime | 2s |
| Inventory → Pricing | Handoff | Hourly | 30s |
| Inventory → Personalization | State Graph | Real-time | 500ms |
| Pricing → Marketing | Handoff | Daily | 60s |
| Marketing → Customer Understanding | Reflection | Post-campaign | N/A |
| All Agents → State Graph | Read/Write | Continuous | 100ms |
