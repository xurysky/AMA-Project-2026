# Recovery Verification — 2026-05-24

## 本地构建检查

命令：

```bash
python3 -m compileall src scripts
```

结果：

```text
OK
```

## Azure 运行时检查

Live demo：

```text
https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/
```

Container App 证据：

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

健康检查：

```bash
curl https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/health
```

观测结果：

```json
{
  "status": "healthy",
  "active_runs": 3,
  "state_store": "cosmos_db"
}
```

## 场景运行检查

命令：

```bash
curl -X POST "https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/api/v1/runs/summer?region=china"
```

观测摘要：

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

## 解读

当前部署已经证明：

- Azure Container Apps 运行时已上线。
- Cosmos DB 状态持久化已启用。
- 可以创建按区域区分的季节性经营场景。
- 运行时暴露了五个 Agent 的 registry。
- 业务决策以 work order 形式等待人工审批。

当前恢复重点是：通过干净的代码库提交和 panel-ready narrative，让这些证据被 mentor 和 panel 清楚看到。

