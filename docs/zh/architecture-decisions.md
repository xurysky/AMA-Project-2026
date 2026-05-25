# Architecture Decisions Record (ADR)

## Overview

This document records the key architectural decisions made in the Autonomous Retail Intelligence Agent Platform, including the rationale, trade-offs, and alternatives considered. Following TOGAF's Architecture Development Method (ADM), each decision traces back to a business requirement.

---

## ADR-001: Multi-Agent Architecture (vs Monolithic)

**Status:** Accepted

**Context:** Contoso Fashion has multiple retail systems (POS, CRM, inventory, pricing, marketing) that currently operate independently. A monolithic AI system would create tight coupling and single points of failure.

**Decision:** Adopt a multi-agent architecture with 5 specialized agents, each owning a specific business domain.

**Rationale:**
- **Separation of Concerns**: Each agent focuses on one domain (customer, personalization, inventory, pricing, marketing)
- **Independent Scaling**: Inventory Agent needs batch processing; Personalization Agent needs real-time response
- **Fault Isolation**: Marketing Agent failure doesn't affect Inventory or Pricing
- **Team Autonomy**: Different teams can develop and deploy agents independently

**Alternatives Considered:**
- Monolithic AI system: Simpler but creates tight coupling, harder to scale
- Microservices without agents: Loses autonomous decision-making capability

**Trade-offs:**
- Added complexity in inter-agent communication
- Need for distributed state management
- Requires orchestration layer (Azure AI Foundry)

---

## ADR-002: Azure AI Foundry as Orchestration Layer

**Status:** Accepted

**Context:** Need a platform to coordinate 5 agents, manage their lifecycle, and provide observability.

**Decision:** Use Azure AI Foundry as the primary orchestration platform.

**Rationale:**
- **Native Azure Integration**: Seamless with OpenAI, Cosmos DB, Event Hubs, APIM
- **Agent Framework**: Built-in support for multi-agent coordination, tool use, memory
- **Enterprise Grade**: SOC 2, ISO 27001, GDPR compliance
- **Managed Service**: Reduces operational overhead vs self-hosted solutions

**Alternatives Considered:**
- LangChain/LangGraph: Open source but requires more infrastructure management
- Custom orchestration: Full control but significant development effort
- AWS Bedrock: Less mature agent framework, no GPT-4o access

---

## ADR-003: A2A Protocol + MCP for Agent Communication

**Status:** Accepted

**Context:** Agents need to communicate with each other and with external tools/APIs.

**Decision:** Use Google's A2A (Agent-to-Agent) Protocol for inter-agent communication and Model Context Protocol (MCP) for tool/API integration.

**Rationale:**
- **A2A**: Standardized protocol for agent discovery, task delegation, and state sharing
- **MCP**: Universal tool interface, framework-agnostic, supports Azure API Management as gateway
- **Decoupling**: Agents don't need to know each other's implementation details
- **Extensibility**: New agents or tools can be added without modifying existing ones

**Alternatives Considered:**
- Direct REST APIs: Simpler but creates tight coupling
- Message queues only (Event Hubs): Good for async but lacks task delegation semantics
- gRPC: High performance but not agent-aware

---

## ADR-004: Cosmos DB for Unified Data Layer

**Status:** Accepted

**Context:** Need a database that handles document storage, vector search, and global distribution for 900+ stores across Asia.

**Decision:** Use Azure Cosmos DB as the primary data store for customer personas, agent state, and vector search.

**Rationale:**
- **Multi-model**: Document + Vector search in one service
- **Global Distribution**: Multi-region writes for Asia-Pacific (East Asia, Southeast Asia)
- **Serverless**: Pay-per-use for variable retail workloads
- **Low Latency**: <10ms point reads for real-time agent decisions

**Alternatives Considered:**
- PostgreSQL + pgvector: Lower cost but requires more management, less global distribution
- Azure Cognitive Search: Better for full-text search but overkill for agent state
- MongoDB Atlas: Similar capabilities but less Azure-native integration

---

## ADR-005: Synthetic Persona for Privacy Compliance

**Status:** Accepted

**Context:** Customer Understanding Agent needs customer data for personalization, but Asia has strict privacy laws (China PIPL, Japan APPI, Singapore PDPA).

**Decision:** Use synthetic personas (TinyTroupe) for cold-start and model training, with real data only for production inference with explicit consent.

**Rationale:**
- **Privacy by Design**: No real PII used for model training
- **Cold Start Solution**: New customers get immediate personalization via synthetic profiles
- **Compliance**: Meets PDPA/PIPL/APPI requirements without complex consent management
- **Testing**: 50+ synthetic personas for comprehensive edge case testing

**Trade-offs:**
- Synthetic data may not capture all real-world diversity
- Requires ongoing validation against real (anonymized) data distributions

---

## ADR-006: Human-in-the-Loop for Critical Decisions

**Status:** Accepted

**Context:** Autonomous agents making pricing or marketing decisions without human oversight could cause significant business impact.

**Decision:** Implement Human-in-the-Loop (HITL) for high-impact decisions (price changes >10%, marketing budget >¥100K, new customer segment targeting).

**Rationale:**
- **Risk Mitigation**: Prevents costly autonomous errors
- **Trust Building**: Retail managers need confidence in agent recommendations
- **Regulatory**: Some decisions require human accountability
- **Learning**: Human feedback improves agent models over time

**Implementation:**
- Approval workflow via Microsoft Teams integration
- Escalation matrix: Agent → Store Manager → Regional Manager
- Timeout policy: Auto-approve after 4 hours if no response (configurable)

---

## ADR-007: Mock-First Development Pattern

**Status:** Accepted

**Context:** Need to develop and test agent logic without dependency on production data or external services.

**Decision:** All external dependencies (Azure OpenAI, Cosmos DB, weather APIs, POS systems) are mocked in development, with integration tests using recorded responses.

**Rationale:**
- **Speed**: No waiting for external service provisioning
- **Cost**: No Azure OpenAI token consumption during development
- **Reliability**: Tests don't fail due to external service outages
- **Reproducibility**: Deterministic test results

**Implementation:**
- Mock classes for all external services
- Recorded response fixtures for integration tests
- Environment-based switching: `MOCK=true` for development, `MOCK=false` for staging/production

---

## ADR-008: Incremental Security Implementation

**Status:** Accepted

**Context:** Full zero-trust security from Day 1 would delay project timeline significantly.

**Decision:** Implement security incrementally across 3 phases, with each phase adding a security layer.

**Rationale:**
- **Pragmatic**: Get working prototype first, harden progressively
- **Risk-based**: Prioritize highest-risk areas first (data access, API authentication)
- **TOGAF-aligned**: Security architecture evolves with the solution

**Phases:**
1. Foundation: Key Vault + Managed Identity + RBAC
2. Hardening: Azure Entra + Purview + Network Isolation
3. Zero Trust: Front Door WAF + DDoS + Full Audit + Pen Testing

---

## Design Patterns Used

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Agent Pattern** | All 5 agents | Autonomous decision-making with defined interfaces |
| **Message Passing** | base_agent.py | Async inter-agent communication via AgentMessage |
| **Observer/Event-Driven** | Event Hubs integration | Decoupled agent notifications |
| **Circuit Breaker** | Agent resilience | Prevent cascade failures |
| **Strategy** | Pricing Agent | Swappable pricing algorithms (rule-based, ML, LLM) |
| **Template Method** | BaseAgent.process() | Standardized agent lifecycle with customizable behavior |
| **Repository** | Data access layer | Abstract data storage from agent logic |
| **Saga** | Multi-agent workflows | Distributed transaction management across agents |
