# Dated acceptance — 2026-11-03

## Passed

- Actual MAF fan-out/fan-in graph on Functions + Azure Durable Task Scheduler.
- Inventory ATP=1,000; eligible audience=280; proposed transfer=320; 15% discount;
  30% discount blocked under the **pilot 20% cap**, not a false margin claim.
- Real hosted GPT-5.4 summary: one application call, 108 input + 149 output =
  **257 total tokens** for the recorded acceptance run. Not a monthly cost quote.
- Waiting review persisted across a Function host restart. Completed node records
  and pending request ID were unchanged. Browser refresh retained the run.
- Actual hosted browser approval button resumed the Durable workflow and produced
  an idempotent demo receipt; production action count=0.
- Real cloud rejection completed with a skipped receipt, no production actions.
- Duplicate request IDs returned the same run. Wrong proposal hash was rejected;
  repeated same approval was idempotent, contradictory rejection refused.
- Anonymous Function access denied, Function-key-without-allowed-owner denied;
  anonymous gateway route denied. Generated SDK public run/respond routes disabled.
- Function-served HTML/JS/CSS hashes matched the accepted local files.
- Gateway candidate internally proxied the health route successfully. Existing
  homepage content hash, AKS proxy configuration, identity, environment, resource
  limits, scale, original environment variables and Entra policy were preserved.
- Chinese/English initial UI at 1440, 1024 and 390px: node selection, no overflow,
  no JS errors. Actual cloud waiting-state UI fixture tested keyboard focus across
  polling and mobile dependency cues. Fresh independent design review passed.

## Important boundaries

Owner's actual interactive Entra/MFA sign-in was not impersonated. Browser
acceptance used privileged deployment-test access, not a claim that MFA was tested.
The canvas visualizes real execution; it cannot edit or publish arbitrary graphs.
Only synthetic data and a demo receipt are involved; it is not a production
inventory, marketing or approval integration. Local graph tests alone did not
establish cloud correctness: live event transport required a JSON normalization
fix, now covered for both mapping and JSON-text replies with strict validation.

Prerelease integration SDKs are pinned in requirements.txt. Upgrade them only
with replay, review and cloud continuation regression. Public TLS Scheduler
network access still requires Managed Identity/RBAC. This pilot does not provide
private endpoints or automatic storage-retention cleanup. No monthly budget cap
is claimed; costs include executions, scheduling, storage, telemetry, traffic
and optional model tokens.

## Rollback

The previous gateway revision `ca-eag-hub--polish1102` is retained. Activate it if
necessary, wait for healthy readiness, then restore 100% traffic to it. The new
route will disappear; the original AMA is not rolled back because it was never
changed. Stop remaining pilot instances separately; traffic rollback does not
remove storage or disable Scheduler billing. Never remove shared secrets,
identities or environment settings during a rollback.
