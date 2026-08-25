"""Script to demonstrate distributed tracing."""
import sys
sys.path.insert(0, ".")

from pipelines.observability_pipeline import ObservabilityPipeline


def main():
    pipeline = ObservabilityPipeline()

    print("=== AI Trace Demo ===\n")

    print("--- Single Request Trace ---")
    result = pipeline.simulate_full_request("Explain our incident response policy")
    trace_id = result["trace_id"]
    print(f"  Trace ID: {trace_id}")

    tree = pipeline.tracer.get_trace_tree(trace_id)
    print(f"  Root Operation: {tree['root_operation']}")
    print(f"  Total Duration: {tree['total_duration_ms']:.1f}ms")
    print(f"  Spans: {tree['span_count']}")
    print(f"  Status: {tree['status']}")

    def print_span_tree(spans, indent=0):
        for span in spans:
            prefix = "  " * indent
            print(f"{prefix}├── {span['name']}: {span['duration_ms']:.1f}ms [{span['status']}]")
            if span.get("attributes"):
                for k, v in span["attributes"].items():
                    print(f"{prefix}│   {k}: {v}")
            if span.get("children"):
                print_span_tree(span["children"], indent + 1)

    print("\n  Trace Tree:")
    print_span_tree(tree["tree"])

    print("\n--- Agent Run Trace ---")
    agent_result = pipeline.simulate_agent_run("research-agent")
    run = pipeline.agent_tracer.get_run_detail(agent_result["trace_id"])
    print(f"  Agent: {run['agent_name']}")
    print(f"  Steps: {run['total_steps']}")
    print(f"  Duration: {run['total_duration_ms']:.1f}ms")
    print(f"  Tokens: {run['total_tokens']}")
    print(f"  Loop Detected: {run['loop_detected']}")
    for step in run["steps"]:
        print(f"    Step {step['step']}: {step['action']} ({step['tool'] or 'reasoning'}) - {step['duration_ms']:.1f}ms")

    print("\n--- LLM Call Trace ---")
    call = pipeline.simulate_llm_call("anthropic", "claude-3-sonnet")
    print(f"  Provider: {call.provider}/{call.model}")
    print(f"  Tokens: {call.input_tokens} input + {call.output_tokens} output")
    print(f"  Latency: {call.latency_ms:.1f}ms")
    print(f"  TTFT: {call.ttft_ms:.1f}ms")
    print(f"  Cost: ${call.cost_usd:.6f}")

    print("\n--- Slowest Traces ---")
    pipeline.simulate_traffic(30)
    slowest = pipeline.tracer.get_slowest_traces(5)
    for t in slowest:
        print(f"  {t['trace_id']}: {t['total_duration_ms']:.1f}ms ({t['span_count']} spans)")


if __name__ == "__main__":
    main()
