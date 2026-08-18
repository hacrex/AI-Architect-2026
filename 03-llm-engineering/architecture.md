# LLM Engineering — Multi-Agent System Architecture

## System overview

```
┌──────────┐    ┌─────────────┐    ┌──────────────────┐
│  User    │───▶│ API Gateway │───▶│ Agent Orchestrator│
└──────────┘    └─────────────┘    └────────┬─────────┘
                                            │
              ┌─────────────────────────────┼─────────────────┐
              │                             │                 │
              ▼                             ▼                 ▼
    ┌──────────────┐            ┌──────────────┐   ┌──────────────┐
    │ Support Agent│            │ Billing Agent│   │ Tech Agent   │
    └──────┬───────┘            └──────┬───────┘   └──────┬───────┘
           │                           │                   │
           ▼                           ▼                   ▼
    ┌──────────────┐            ┌──────────────┐   ┌──────────────┐
    │ Knowledge DB │            │ Order DB     │   │ Code Repo   │
    └──────────────┘            └──────────────┘   └──────────────┘
```

## Failure handling

- Agent timeout → fallback to default response
- Agent error → retry with exponential backoff
- Agent unavailable → route to alternate agent or human escalation
- Knowledge base down → return cached responses only
