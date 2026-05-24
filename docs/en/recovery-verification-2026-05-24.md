# Recovery Verification — 2026-05-24

## Local Build Check

Command:

```bash
python3 -m compileall src scripts
```

Result:

```text
OK
```

## Azure Runtime Check

Live demo:

```text
https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/
```

Container App evidence:

```json
{
  "name": "ama-retail-control-tower",
  "url": "ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io",
  "provisioning": "Succeeded",
  "running": "Running",
  "image": "amaregistry.azurecr.io/ama-retail-agent:20260519-120038",
  "latestRevision": "ama-retail-control-tower--0000006"
}
```

Health endpoint:

```bash
curl https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/health
```

Observed response:

```json
{
  "status": "healthy",
  "active_runs": 3,
  "state_store": "cosmos_db"
}
```

## Scenario Run Check

Command:

```bash
curl -X POST "https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/api/v1/runs/summer?region=china"
```

Observed summary:

```json
{
  "run_id": "RUN-879215F5",
  "status": "WAITING_FOR_DECISION",
  "region": "china",
  "work_orders": 9,
  "agents": [
    "Inventory Agent",
    "Pricing Agent",
    "Customer Understanding Agent",
    "Personalization Agent",
    "Marketing Agent"
  ]
}
```

## Interpretation

The current deployment demonstrates:

- A running Azure Container Apps runtime.
- Cosmos DB-backed state persistence.
- Region-aware seasonal run creation.
- Five-agent registry exposed through the runtime.
- Work-order based decision flow waiting for human approval.

The immediate recovery priority is to make this evidence visible through a clean repository commit and panel-ready narrative.

