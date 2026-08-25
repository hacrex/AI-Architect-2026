"""Agent Trace — observe multi-step agent workflows, tool calls, and loops."""
import uuid
from datetime import datetime
from typing import Optional
from app.models import AgentStep, AgentRun, TraceStatus
import config.settings as settings


class AgentTracer:
    """Trace agent workflows with step-by-step visibility and loop detection."""

    def __init__(self):
        self._runs: dict[str, AgentRun] = {}
        self._active_run: Optional[AgentRun] = None

    def start_run(self, agent_name: str, trace_id: str = "") -> str:
        run = AgentRun(
            trace_id=trace_id or uuid.uuid4().hex[:16],
            agent_name=agent_name
        )
        self._runs[run.trace_id] = run
        self._active_run = run
        return run.trace_id

    def add_step(self, action: str, tool_name: str = "", tool_input: str = "",
                 tool_output: str = "", reasoning: str = "",
                 duration_ms: float = 0.0, tokens_used: int = 0,
                 status: TraceStatus = TraceStatus.OK) -> AgentStep:
        if not self._active_run:
            return None
        step = AgentStep(
            step_number=len(self._active_run.steps) + 1,
            action=action,
            tool_name=tool_name,
            tool_input=tool_input[:500] if tool_input else "",
            tool_output=tool_output[:500] if tool_output else "",
            reasoning=reasoning[:500] if reasoning else "",
            duration_ms=duration_ms,
            status=status,
            tokens_used=tokens_used
        )
        self._active_run.steps.append(step)
        self._active_run.total_steps = len(self._active_run.steps)
        self._active_run.total_duration_ms += duration_ms
        self._active_run.total_tokens += tokens_used
        return step

    def end_run(self, status: TraceStatus = TraceStatus.OK):
        if not self._active_run:
            return
        self._active_run.status = status
        self._detect_loops()
        self._active_run = None

    def _detect_loops(self):
        if not self._active_run:
            return
        actions = [s.action for s in self._active_run.steps]
        seen = {}
        loop_count = 0
        for a in actions:
            seen[a] = seen.get(a, 0) + 1
            if seen[a] >= settings.AGENT_LOOP_THRESHOLD:
                loop_count += 1
        if loop_count > 0:
            self._active_run.loop_detected = True
            self._active_run.loop_count = loop_count

    def get_run(self, trace_id: str) -> Optional[AgentRun]:
        return self._runs.get(trace_id)

    def get_run_detail(self, trace_id: str) -> dict:
        run = self._runs.get(trace_id)
        if not run:
            return {"error": f"Run {trace_id} not found"}
        return {
            "trace_id": run.trace_id,
            "agent_name": run.agent_name,
            "total_steps": run.total_steps,
            "total_duration_ms": round(run.total_duration_ms, 2),
            "total_tokens": run.total_tokens,
            "status": run.status.value,
            "loop_detected": run.loop_detected,
            "loop_count": run.loop_count,
            "timestamp": run.timestamp.isoformat(),
            "steps": [
                {
                    "step": s.step_number,
                    "action": s.action,
                    "tool": s.tool_name,
                    "duration_ms": round(s.duration_ms, 2),
                    "tokens": s.tokens_used,
                    "status": s.status.value,
                    "reasoning_preview": s.reasoning[:100] if s.reasoning else ""
                }
                for s in run.steps
            ]
        }

    def get_summary(self) -> dict:
        runs = list(self._runs.values())
        if not runs:
            return {"total_runs": 0}
        total_steps = sum(r.total_steps for r in runs)
        total_tokens = sum(r.total_tokens for r in runs)
        loops = sum(1 for r in runs if r.loop_detected)
        durations = [r.total_duration_ms for r in runs if r.total_duration_ms > 0]
        return {
            "total_runs": len(runs),
            "total_steps": total_steps,
            "total_tokens": total_tokens,
            "avg_steps_per_run": round(total_steps / len(runs), 1) if runs else 0,
            "avg_duration_ms": round(sum(durations) / len(durations), 1) if durations else 0,
            "loop_detected_runs": loops,
            "loop_rate_pct": round(loops / len(runs) * 100, 1) if runs else 0,
            "error_runs": sum(1 for r in runs if r.status == TraceStatus.ERROR),
        }

    def get_tool_usage(self) -> dict:
        tool_counts = {}
        tool_tokens = {}
        for run in self._runs.values():
            for step in run.steps:
                if step.tool_name:
                    tool_counts[step.tool_name] = tool_counts.get(step.tool_name, 0) + 1
                    tool_tokens[step.tool_name] = tool_tokens.get(step.tool_name, 0) + step.tokens_used
        return {
            tool: {"calls": count, "tokens": tool_tokens.get(tool, 0)}
            for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
        }

    def list_runs(self, limit: int = 50) -> list[dict]:
        runs = sorted(self._runs.values(),
                      key=lambda r: r.timestamp, reverse=True)[:limit]
        return [
            {
                "trace_id": r.trace_id,
                "agent_name": r.agent_name,
                "total_steps": r.total_steps,
                "total_duration_ms": round(r.total_duration_ms, 2),
                "status": r.status.value,
                "loop_detected": r.loop_detected,
                "timestamp": r.timestamp.isoformat()
            }
            for r in runs
        ]
