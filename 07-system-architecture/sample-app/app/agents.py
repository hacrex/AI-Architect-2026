"""Agent subsystem — planning, tool execution, and guardrails."""
import uuid
import random
from datetime import datetime
from typing import Optional
from app.models import AgentPlan, AgentExecution, AgentAction


class ToolRegistry:
    """Registry of available tools for agents."""

    def __init__(self):
        self._tools: dict[str, dict] = {
            "search": {
                "name": "search",
                "description": "Search internal knowledge base",
                "requires_approval": False,
                "max_calls_per_request": 3,
                "category": "read"
            },
            "database": {
                "name": "database",
                "description": "Query internal databases",
                "requires_approval": False,
                "max_calls_per_request": 2,
                "category": "read"
            },
            "api_call": {
                "name": "api_call",
                "description": "Call external APIs",
                "requires_approval": True,
                "max_calls_per_request": 2,
                "category": "write"
            },
            "email": {
                "name": "email",
                "description": "Send emails on behalf of user",
                "requires_approval": True,
                "max_calls_per_request": 1,
                "category": "write"
            },
            "create_ticket": {
                "name": "create_ticket",
                "description": "Create Jira/ServiceNow tickets",
                "requires_approval": True,
                "max_calls_per_request": 1,
                "category": "write"
            },
            "deploy": {
                "name": "deploy",
                "description": "Trigger deployment (HIGHLY RESTRICTED)",
                "requires_approval": True,
                "max_calls_per_request": 0,
                "category": "admin"
            }
        }

    def get_tool(self, name: str) -> Optional[dict]:
        return self._tools.get(name)

    def list_tools(self) -> dict[str, dict]:
        return self._tools

    def can_use_tool(self, tool_name: str, user_roles: list[str]) -> dict:
        tool = self._tools.get(tool_name)
        if not tool:
            return {"allowed": False, "reason": "tool_not_found"}

        if tool["category"] == "admin" and "admin" not in user_roles:
            return {"allowed": False, "reason": "insufficient_permissions"}

        if tool["requires_approval"] and "admin" not in user_roles:
            return {"allowed": False, "reason": "requires_approval", "requires_human": True}

        return {"allowed": True}


class AgentGuardrails:
    """Guardrails for agent behavior."""

    def __init__(self):
        self._max_steps = 5
        self._max_tool_calls = 10
        self._blocked_actions = ["deploy", "delete", "production_access"]

    def check_plan(self, plan: AgentPlan, user_roles: list[str]) -> dict:
        violations = []

        if len(plan.steps) > self._max_steps:
            violations.append(f"plan_exceeds_max_steps:{len(plan.steps)}/{self._max_steps}")

        if plan.estimated_tokens > 8000:
            violations.append(f"estimated_tokens_too_high:{plan.estimated_tokens}")

        return {
            "approved": len(violations) == 0,
            "violations": violations
        }

    def check_execution_step(self, step: dict) -> dict:
        action = step.get("action", "")

        if action in self._blocked_actions:
            return {
                "allowed": False,
                "reason": f"blocked_action:{action}",
                "requires_human": True
            }

        return {"allowed": True}


class AgentPlanner:
    """Plan agent execution steps."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def plan(self, query: str, context: str = "") -> AgentPlan:
        steps = []
        tools_needed = []

        steps.append({
            "step": 1,
            "action": "analyze_query",
            "description": "Understand the user's question",
            "tool": None
        })

        if "search" in query.lower() or "find" in query.lower() or "what" in query.lower():
            steps.append({
                "step": 2,
                "action": "search",
                "description": "Search knowledge base for relevant information",
                "tool": "search"
            })
            tools_needed.append("search")

        if "database" in query.lower() or "data" in query.lower():
            steps.append({
                "step": len(steps) + 1,
                "action": "database",
                "description": "Query database for structured data",
                "tool": "database"
            })
            tools_needed.append("database")

        if "email" in query.lower() or "send" in query.lower():
            steps.append({
                "step": len(steps) + 1,
                "action": "email",
                "description": "Compose and send email",
                "tool": "email"
            })
            tools_needed.append("email")

        steps.append({
            "step": len(steps) + 1,
            "action": "synthesize",
            "description": "Synthesize information into a response",
            "tool": None
        })

        return AgentPlan(
            steps=steps,
            tools_needed=tools_needed,
            estimated_tokens=len(query.split()) * 100 + len(context.split()) * 50
        )


class AgentExecutor:
    """Execute agent plans."""

    def __init__(self, tool_registry: ToolRegistry, guardrails: AgentGuardrails):
        self.tool_registry = tool_registry
        self.guardrails = guardrails
        self._executions: list[AgentExecution] = []

    def execute(self, plan: AgentPlan, query: str, context: str,
                user_roles: list[str]) -> AgentExecution:
        approval_check = self.guardrails.check_plan(plan, user_roles)

        results = []
        total_tokens = 0
        total_tool_calls = 0

        for step in plan.steps:
            tool_name = step.get("tool")

            if tool_name:
                tool_check = self.tool_registry.can_use_tool(tool_name, user_roles)
                if not tool_check["allowed"]:
                    results.append({
                        "step": step["step"],
                        "action": step["action"],
                        "status": "blocked",
                        "reason": tool_check.get("reason", "unknown")
                    })
                    continue

                tool_result = self._execute_tool(tool_name, query, context)
                results.append(tool_result)
                total_tool_calls += 1
                total_tokens += tool_result.get("tokens", 0)
            else:
                results.append({
                    "step": step["step"],
                    "action": step["action"],
                    "status": "completed",
                    "result": f"Executed {step['action']}"
                })
                total_tokens += 50

        final_answer = self._synthesize_answer(query, context, results)
        total_tokens += len(final_answer.split()) * 2

        execution = AgentExecution(
            plan=plan,
            results=results,
            final_answer=final_answer,
            total_tokens=total_tokens,
            total_tool_calls=total_tool_calls
        )
        self._executions.append(execution)
        return execution

    def _execute_tool(self, tool_name: str, query: str, context: str) -> dict:
        if tool_name == "search":
            return {
                "step": 0,
                "action": "search",
                "status": "completed",
                "result": f"Found 3 relevant documents for: {query[:50]}",
                "tokens": 150
            }
        elif tool_name == "database":
            return {
                "step": 0,
                "action": "database",
                "status": "completed",
                "result": "Query returned 5 rows",
                "tokens": 100
            }
        elif tool_name == "email":
            return {
                "step": 0,
                "action": "email",
                "status": "pending_approval",
                "result": "Email draft created, awaiting approval",
                "tokens": 80
            }
        else:
            return {
                "step": 0,
                "action": tool_name,
                "status": "completed",
                "result": f"Tool {tool_name} executed",
                "tokens": 50
            }

    def _synthesize_answer(self, query: str, context: str, results: list[dict]) -> str:
        completed = [r for r in results if r.get("status") == "completed"]
        return f"Based on {len(completed)} sources, here is the answer to: {query[:100]}"

    def get_executions(self) -> list[AgentExecution]:
        return self._executions


class AgentService:
    """Complete agent subsystem."""

    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.guardrails = AgentGuardrails()
        self.planner = AgentPlanner(self.tool_registry)
        self.executor = AgentExecutor(self.tool_registry, self.guardrails)

    def run(self, query: str, context: str = "", user_roles: list[str] = None) -> dict:
        roles = user_roles or ["all"]

        plan = self.planner.plan(query, context)

        approval = self.guardrails.check_plan(plan, roles)

        execution = self.executor.execute(plan, query, context, roles)

        return {
            "query": query,
            "plan_steps": len(plan.steps),
            "tools_needed": plan.tools_needed,
            "plan_approved": approval["approved"],
            "execution": {
                "results": execution.results,
                "final_answer": execution.final_answer,
                "total_tokens": execution.total_tokens,
                "total_tool_calls": execution.total_tool_calls
            }
        }

    def get_tools(self) -> dict:
        return self.tool_registry.list_tools()

    def get_stats(self) -> dict:
        return {
            "total_executions": len(self.executor.get_executions()),
            "available_tools": len(self.tool_registry.list_tools()),
            "blocked_actions": self.guardrails._blocked_actions
        }
