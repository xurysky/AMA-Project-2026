# AMA Durable runtime pilot

An isolated customer-demo runtime canvas, not a Dify-style workflow editor.
The existing AMA application is unchanged. All inputs are **synthetic** and the
only final write is an idempotent demo receipt. No WMS/CRM actions are sent.

## Execution

```
Snapshot ─┬─ Inventory → Pricing ────────┐
          └─ Customer → Personalization ┤
                                      ↓
                             Proposal → Policy → Review → Demo receipt
```

The graph uses Microsoft Agent Framework executors, fan-out/fan-in and HITL.
The official Azure Functions Durable extension runs the graph, with Azure Durable
Task Scheduler as checkpoint backend. Deterministic inventory, price and consent
checks do not call a model. An optional Marketing Agent makes **one** bounded
summary request to the existing model deployment; a failed model call is a failed
node, not a canned response presented as generated text.

Blob node records are an observational read model. They do not drive transitions.
The browser polls real status and preserves completed node outputs after refresh.
Short activities can finish between polls. There are no fabricated delays.

### Policy nuance

The legacy fixture's narrative claims a 30% markdown violates margin, but the
supplied numbers do not support that claim. This pilot calculates the margin and
blocks 30% under an explicitly new **pilot 20% discount cap**. It does not silently
change the original AMA policy engine. The sample's old recommendations are not
used as authoritative policy results.

## Security and limits

- Existing gateway Entra authentication plus a single allowed principal.
- Function key is held only by the gateway; never in browser JS or Git.
- Every run is owner-bound. UUID request IDs map to stable server run IDs.
- One active run per owner, 20 new requests/day (application quota, not a billing cap).
- Review compares proposal hash and one-hour expiry, and records the trusted actor.
- Duplicate decision deliveries are idempotent; contradictory decisions are refused.
- Approval is **pilot reviewer** authority, not a grant of production business rights.
- Generated SDK start/respond endpoints are disabled; only guarded custom routes exist.
- Durable events can arrive as mappings or JSON text. The application normalizes
  one JSON layer and then validates an extra-forbidden, strict Pydantic Decision.
  No pickle/custom type decoding is performed on replies.
- Expiry prevents late review; it is not automatic instance termination. A stop
  action is provided. Blob retention cleanup is not implemented in this pilot.
- Model request timeout 75s; output budget 800 tokens; SDK HTTP retries disabled.
  Durable activity redelivery is still possible after a host failure, so this is
  not an exactly-once guarantee for upstream model billing.

## Local verification

Python 3.12:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python tests/test_graph.py
```

The graph test replaces Blob writes only; it checks actual MAF fan-in, numerical
rules, approval/rejection and the absence of production actions. It is not proof
of Azure replay/approval integration; deployment acceptance must also exercise the
real Scheduler and hosted extension.

## Configuration (values must remain outside Git)

Required Function app settings:
`AzureWebJobsStorage`, `DURABLE_TASK_SCHEDULER_CONNECTION_STRING`,
`PILOT_ALLOWED_PRINCIPALS`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`,
`AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_VERSION`.

Use managed identity + Durable Task Data Contributor for Scheduler access.
The gateway needs a secret-backed `AMA_WORKFLOW_FUNCTION_KEY` and must overwrite
or supply identity headers only after platform authentication. Never expose the
plain Nginx container as an unauthenticated public gateway.

`gateway/` derives from the existing gateway's pinned immutable image; it retains
home assets and the AKS proxy. The runtime route is `/ama-workflow/`. Deployment
requires an explicit base-image digest and a source revision/build-context hash.

See `deployment.json` and `ACCEPTANCE.md` for the dated deployed observation and
its verification scope. This is a separately billed Consumption pilot, not an
upgrade of the existing AMA container or a production business integration.

## Cost boundary

New resources are Functions Flex Consumption (always-ready = 0), Scheduler
Consumption and LRS storage. Execution, orchestration actions, storage operations,
telemetry and cross-region gateway traffic can incur charges. Model summaries
reuse the existing deployment but incur their own token usage. No extra VM,
AKS, GPU or Dedicated scheduler capacity is provisioned. A daily application
quota is not a hard Azure budget cap. There is no verified monthly price quote.

The gateway candidate briefly runs alongside the prior revision during validation.
After release the old revision can be deactivated while retaining it as rollback.
Rolling back traffic hides this route; it does not delete storage or cancel
outstanding Durable instances. Stop active pilot runs separately when retiring it.
