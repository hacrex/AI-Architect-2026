import httpx
import json
import time

BASE_URL = "http://localhost:8002"


def test_health():
    """Test health endpoint."""
    response = httpx.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")
    return data


def test_agents():
    """Test list agents endpoint."""
    response = httpx.get(f"{BASE_URL}/agents")
    assert response.status_code == 200
    agents = response.json()
    print(f"✓ Found {len(agents)} agents")
    for agent in agents:
        print(f"  - {agent['name']}: {agent['tools']}")
    return agents


def test_tools():
    """Test list tools endpoint."""
    response = httpx.get(f"{BASE_URL}/tools")
    assert response.status_code == 200
    tools = response.json()
    print(f"✓ Found {len(tools)} tools")
    for tool in tools:
        print(f"  - {tool['name']}")
    return tools


def test_simple_query():
    """Test simple single-agent query."""
    print("\n--- Test: Simple Query ---")
    response = httpx.post(
        f"{BASE_URL}/query",
        json={"query": "What is the leave policy?"},
        timeout=30.0,
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Agent used: {data['agent_used']}")
    print(f"  Tokens: {data['tokens_used']}")
    print(f"  Latency: {data['latency_ms']}ms")
    print(f"  Tool calls: {len(data['tool_calls'])}")
    return data


def test_multi_agent_query():
    """Test multi-agent orchestration."""
    print("\n--- Test: Multi-Agent Query ---")
    response = httpx.post(
        f"{BASE_URL}/query",
        json={"query": "Check my order status and explain the return policy"},
        timeout=60.0,
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Agents used: {data['agent_used']}")
    print(f"  Plan: {data['orchestration_plan']}")
    print(f"  Tool calls: {len(data['tool_calls'])}")
    return data


def test_direct_agent():
    """Test direct agent query."""
    print("\n--- Test: Direct Agent Query ---")
    response = httpx.post(
        f"{BASE_URL}/agent/tech",
        json={"query": "Search for authentication code examples"},
        timeout=30.0,
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Agent: {data['agent_used']}")
    print(f"  Tool calls: {len(data['tool_calls'])}")
    return data


if __name__ == "__main__":
    print("=== LLM Engineering — Multi-Agent System Tests ===\n")

    try:
        test_health()
        test_agents()
        test_tools()
        test_simple_query()
        test_multi_agent_query()
        test_direct_agent()
        print("\n✓ All tests passed!")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
