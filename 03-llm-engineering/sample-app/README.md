# LLM Engineering — Multi-Agent Sample App

A working prototype demonstrating **multi-agent orchestration**, **tool use**, and **context engineering** from Day 03.

> **Building on Day 02**: This app extends the Model Router from Day 02 (`02-ai-ml/sample-app/`) by adding agent orchestration, tool calling, and advanced RAG patterns.

## Architecture

```
User Request
      │
      ▼
┌─────────────────────────────────────────┐
│           FastAPI Gateway               │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │      Agent Orchestrator           │  │
│  │  (routes to specialized agents)   │  │
│  └───────────────────────────────────┘  │
│              │                          │
│    ┌─────────┼─────────┐                │
│    ▼         ▼         ▼                │
│ ┌──────┐ ┌──────┐ ┌──────┐             │
│ │Support│ │Billing│ │Tech  │             │
│ │Agent │ │Agent │ │Agent │             │
│ └──┬───┘ └──┬───┘ └──┬───┘             │
│    │        │        │                  │
│    ▼        ▼        ▼                  │
│ ┌──────┐ ┌──────┐ ┌──────┐             │
│ │Tools │ │Tools │ │Tools │             │
│ │Search│ │Lookup│ │Code  │             │
│ │Docs  │ │Orders│ │Search│             │
│ └──────┘ └──────┘ └──────┘             │
└─────────────────────────────────────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── orchestrator.py      # Agent orchestration logic
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Base agent class
│   │   ├── support.py       # Support agent
│   │   ├── billing.py       # Billing agent
│   │   └── tech.py          # Technical agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py          # Base tool class
│   │   ├── search_docs.py   # Document search tool
│   │   ├── lookup_orders.py # Order lookup tool
│   │   └── code_search.py   # Code search tool
│   └── context.py           # Context engineering utilities
├── config/
│   ├── settings.py          # Configuration management
│   └── .env.example         # Environment variables template
├── docs/
│   └── sample-knowledge.json # Sample knowledge base
├── requirements.txt
└── test_agents.py           # Test script
```

## Quick Start

### 1. Install Dependencies

```bash
cd 03-llm-engineering/sample-app
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

### 3. Start the Server

```bash
uvicorn app.main:app --reload --port 8002
```

### 4. Test the API

```bash
python test_agents.py
```

Or manually:

```bash
# Health check
curl http://localhost:8002/health

# Simple query (auto- routed to appropriate agent)
curl -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the refund policy?"}'

# Multi-step query (orchestrator decomposes)
curl -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Check my order status and explain the return policy"}'

# Direct agent query
curl -X POST http://localhost:8002/agent/support \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I reset my password?"}'

# List available tools
curl http://localhost:8002/tools

# List available agents
curl http://localhost:8002/agents
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with agent status |
| `/query` | POST | Multi-agent query with orchestration |
| `/query/stream` | POST | Streaming multi-agent response |
| `/agent/{agent_name}` | POST | Direct query to specific agent |
| `/agents` | GET | List available agents and capabilities |
| `/tools` | GET | List available tools |
| `/orchestrate` | POST | Explicit orchestration with plan |

## Agent Specialization

### Support Agent
- Handles general questions, policies, how-to guides
- Tools: document search, FAQ lookup
- Model: Balanced (GPT-4)

### Billing Agent
- Handles billing inquiries, order status, refunds
- Tools: order lookup, account lookup
- Model: Precise (GPT-4)

### Technical Agent
- Handles technical questions, code help, debugging
- Tools: code search, documentation search
- Model: Technical (GPT-4)

## Tool Use Pattern

```python
# Tools are defined with schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search internal documents",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "category": {"type": "string"}
                }
            }
        }
    }
]

# Agent decides which tool to call
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=tools,
    tool_choice="auto"
)
```

## Context Engineering

### Context Window Budget
```
Total Context (128K tokens)
├── System Instructions: 5-10%
├── Agent Persona: 5-10%
├── Conversation History: 20-30%
├── Retrieved Documents: 30-40%
├── Tool Results: 10-15%
└── Response Buffer: 20-30%
```

### Context Compression
When context exceeds budget:
1. Summarize older conversation turns
2. Deduplicate retrieved documents
3. Prioritize most relevant context
4. Truncate tool results

## Architecture Patterns Demonstrated

| Pattern | Implementation |
|---------|----------------|
| **Multi-Agent** | Specialized agents for different domains |
| **Orchestration** | Router determines agent selection |
| **Tool Use** | Function calling for external operations |
| **Context Engineering** | Budget management, compression |
| **Handoffs** | Agents can delegate to other agents |
| **State Management** | Conversation history per session |

## Sample Queries

### Simple (Single Agent)
```json
{"query": "What is the leave policy?"}
{"query": "How do I request access to AWS?"}
```

### Multi-Step (Orchestrated)
```json
{"query": "Check my recent orders and explain the return policy for electronics"}
{"query": "Search for Python authentication examples and explain best practices"}
```

### Tool-Heavy
```json
{"query": "Look up order #12345, check if it's eligible for return, and explain the process"}
{"query": "Find all API rate limiting code in the codebase and suggest improvements"}
```

## Key Concepts (Day 03)

This sample app demonstrates:

1. **Multi-Agent Systems** — Specialized agents with distinct capabilities
2. **Agent Orchestration** — Intelligent routing based on query intent
3. **Tool Use** — Function calling for external data and operations
4. **Context Engineering** — Managing context windows efficiently
5. **Handoffs** — Agents delegating to other agents when needed
6. **State Management** — Conversation history and memory
7. **Graceful Degradation** — Fallbacks when agents or tools fail
