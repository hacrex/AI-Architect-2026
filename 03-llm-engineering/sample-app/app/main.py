from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
import logging

from app.models import QueryRequest, QueryResponse, AgentInfo, ToolInfo
from app.orchestrator import Orchestrator
from app.tools import SearchDocsTool, LookupOrdersTool, CodeSearchTool
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM Engineering — Multi-Agent System",
    description="Day 03 - Multi-agent orchestration, tool use, and context engineering",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

# Register tools with agents
search_docs = SearchDocsTool()
lookup_orders = LookupOrdersTool()
code_search = CodeSearchTool()

# Register tools with appropriate agents
orchestrator.agents["support"].register_tool("search_documents", search_docs.execute)
orchestrator.agents["billing"].register_tool("lookup_order", lookup_orders.execute)
orchestrator.agents["tech"].register_tool("search_code", code_search.execute)


@app.get("/health")
async def health_check():
    """Health check with agent status."""
    return {
        "status": "healthy",
        "version": "0.3.0",
        "agents": [info["name"] for info in orchestrator.get_agent_info()],
    }


@app.post("/query", response_model=QueryResponse)
async def query_system(request: QueryRequest):
    """Multi-agent query with orchestration."""
    start_time = time.time()

    try:
        result = await orchestrator.process(request)

        return QueryResponse(
            answer=result["answer"],
            agent_used=", ".join(result["agents_used"]),
            orchestration_plan=result["orchestration_plan"],
            tool_calls=result["tool_calls"],
            tokens_used=result["tokens_used"],
            latency_ms=result["latency_ms"],
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/stream")
async def query_stream(request: QueryRequest):
    """Streaming multi-agent response."""
    async def generate_stream():
        result = await orchestrator.process(request)
        # In a real implementation, this would stream token by token
        yield result["answer"]

    return StreamingResponse(generate_stream(), media_type="text/event-stream")


@app.post("/agent/{agent_name}", response_model=QueryResponse)
async def query_direct_agent(agent_name: str, request: QueryRequest):
    """Direct query to a specific agent."""
    from app.models import AgentType

    try:
        agent_type = AgentType(agent_name)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown agent: {agent_name}")

    agent = orchestrator.agents.get(agent_type)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_name}")

    start_time = time.time()
    response = await agent.process(request.query, request.context)

    return QueryResponse(
        answer=response.content,
        agent_used=agent_name,
        tool_calls=response.tool_calls,
        tokens_used=response.tokens_used,
        latency_ms=response.latency_ms,
    )


@app.get("/agents")
async def list_agents():
    """List available agents and their capabilities."""
    return orchestrator.get_agent_info()


@app.get("/tools")
async def list_tools():
    """List available tools."""
    tools = [
        ToolInfo(
            name="search_documents",
            description="Search internal company documents for relevant information",
            parameters={"query": "string", "category": "string (optional)"},
        ),
        ToolInfo(
            name="lookup_order",
            description="Look up order details by order ID",
            parameters={"order_id": "string"},
        ),
        ToolInfo(
            name="search_code",
            description="Search code repositories for relevant code examples",
            parameters={"query": "string", "language": "string (optional)", "repository": "string (optional)"},
        ),
    ]
    return tools


@app.post("/orchestrate")
async def orchestrate_explicit(request: QueryRequest):
    """Explicit orchestration with visible plan."""
    result = await orchestrator.process(request)
    return {
        "plan": result["orchestration_plan"],
        "agents_used": result["agents_used"],
        "answer": result["answer"],
        "tool_calls": result["tool_calls"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
