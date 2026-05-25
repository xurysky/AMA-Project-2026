# CI/CD & Day 2 Operations

## Overview

The Autonomous Retail Intelligence Agent Platform uses **GitHub Actions** for CI/CD automation and implements comprehensive **Day 2 Operations** practices for ongoing management, updates, and incident response.

---

## 1. CI/CD Pipeline

### Pipeline Architecture
```
Developer Push → GitHub Actions Trigger
    ├── Stage 1: Code Quality
    │   ├── Linting (ESLint + Pylint)
    │   ├── Type checking (mypy / strict TypeScript)
    │   └── Dependency audit (npm audit / safety check)
    │
    ├── Stage 2: Security Scanning
    │   ├── GitHub Advanced Security (SAST)
    │   ├── OWASP dependency check
    │   └── Secret scanning (prevent leaked credentials)
    │
    ├── Stage 3: Testing
    │   ├── Unit tests (agent behavior)
    │   ├── Integration tests (agent-to-agent handoff)
    │   ├── Contract tests (API schemas)
    │   └── Performance benchmarks (latency targets)
    │
    ├── Stage 4: Build & Package
    │   ├── Docker image build
    │   ├── Push to Azure Container Registry
    │   └── Tag with commit SHA + semantic version
    │
    └── Stage 5: Deploy (conditional)
        ├── Staging → Auto-deploy
        ├── Canary (5% traffic) → Auto-deploy after staging success
        └── Production → Manual approval gate
```

### GitHub Actions Workflow
```yaml
name: Agent CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint & Type Check
        run: npm run lint && npm run typecheck
      - name: Dependency Audit
        run: npm audit --audit-level=high

  security:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - name: GitHub Advanced Security
        uses: github/codeql-action/analyze@v3
      - name: Secret Scanning
        uses: trufflesecurity/trufflehog@main

  test:
    needs: security
    runs-on: ubuntu-latest
    steps:
      - name: Unit Tests
        run: npm test -- --coverage
      - name: Integration Tests
        run: npm run test:integration
      - name: Performance Benchmarks
        run: npm run test:perf

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Build & Push Container
        run: |
          docker build -t ama-agent:${{ github.sha }} .
          docker push amaacr.azurecr.io/ama-agent:${{ github.sha }}
      - name: Deploy to Staging
        run: az containerapp update --image amaacr.azurecr.io/ama-agent:${{ github.sha }}
      - name: Canary Deploy (5%)
        run: az containerapp ingress traffic set --traffic-weight staging=5
      - name: Production Deploy (requires approval)
        uses: trstringer/manual-approval@v1
        with:
          approvers: yuan-wang,tech-lead
```

### Branch Protection Rules
- `main` branch: requires PR + 1 approval + all checks passing
- No direct pushes to main
- Status checks: lint, security scan, tests, performance benchmarks
- Auto-merge after approval + checks

---

## 2. Deployment Strategy

### Environment Tiers
| Environment | Purpose | Deployment | Traffic |
|-------------|---------|------------|---------|
| **Dev** | Feature development | Auto on PR | Developers only |
| **Staging** | Integration testing | Auto on merge to main | Internal testers |
| **Canary** | Production validation | Auto after staging | 5% of production traffic |
| **Production** | Live serving | Manual approval | 100% |

### Canary Deployment Flow
```
1. New version deployed to staging → automated tests pass
2. Shift 5% production traffic to new version (canary)
3. Monitor for 15 minutes:
   - Error rate < 0.1%
   - Latency p95 < 2s
   - No business metric degradation
4. If healthy → shift 25% → 50% → 100%
5. If unhealthy → auto-rollback to previous version
```

### Rollback Strategy
| Scenario | Action | Time |
|----------|--------|------|
| Canary failure | Auto-rollback to previous version | < 1 min |
| Production incident | Manual rollback via Azure CLI | < 5 min |
| Data corruption | Restore from Cosmos DB point-in-time backup | < 30 min |

---

## 3. Day 2 Operations

### Operational Runbooks

#### Agent Update Process
```
1. Developer creates feature branch
2. Code change + tests → PR → review → merge
3. CI/CD pipeline: build → test → deploy to staging
4. Staging validation (automated + manual)
5. Canary deployment (5% traffic, 15 min observation)
6. Gradual rollout (25% → 50% → 100%)
7. Post-deployment monitoring (30 min)
```

#### Incident Response
| Severity | Definition | Response Time | Actions |
|----------|-----------|---------------|---------|
| **P1 (Critical)** | Agent down, data loss | < 15 min | Page on-call, create incident, begin mitigation |
| **P2 (High)** | Degraded performance | < 1 hour | Notify team, investigate, mitigate |
| **P3 (Medium)** | Non-critical error | < 4 hours | Log, prioritize in next sprint |
| **P4 (Low)** | Cosmetic issue | Next sprint | Backlog |

#### On-Call Rotation
- 24/7 on-call coverage (Asia timezone focus)
- Escalation: On-call → Tech Lead → Engineering Manager
- Post-incident review (blameless) within 48 hours

### Configuration Management
- All agent configurations stored in Azure App Configuration
- Feature flags for gradual rollout of new agent capabilities
- A/B testing framework for agent behavior changes
- Configuration version control with rollback capability

### Capacity Planning
| Resource | Current | Scale Trigger | Max |
|----------|---------|---------------|-----|
| Agent replicas | 2 per agent | CPU > 70% | 20 per agent |
| Cosmos DB RU/s | 4,000 | Throttling detected | 40,000 |
| OpenAI tokens/day | 1M | 80% budget consumed | 5M |
| Redis cache | 6GB | Hit rate < 80% | 26GB |

---

## 4. Observability Integration

### Deployment Markers
Every deployment creates a marker in Azure Monitor, enabling correlation between deployments and metric changes.

### Post-Deployment Validation
Automated checks after every deployment:
- Health endpoint returns 200
- Agent latency p95 < 2s (5-minute window)
- Error rate < 0.1% (5-minute window)
- Business metrics within expected range

---

## References

- GitHub Actions Documentation: https://docs.github.com/en/actions
- Azure Container Apps Deployment: https://learn.microsoft.com/azure/container-apps/
- Canary Deployment Pattern: Based on Foundry Gateway (Foundry AI Gateway) design reference
