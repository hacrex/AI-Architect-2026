"""Capacity Planner — estimate infrastructure needs and find bottlenecks."""
import math
from app.models import CapacityEstimate, ScalePlan
import config.settings as settings


class CapacityPlanner:
    """Plan capacity for scaling AI systems."""

    def __init__(self):
        self.baseline_rps = settings.BASELINE_REQUESTS_PER_SEC
        self.peak_multiplier = settings.PEAK_MULTIPLIER
        self.avg_input_tokens = settings.AVG_INPUT_TOKENS_PER_REQUEST
        self.avg_output_tokens = settings.AVG_OUTPUT_TOKENS_PER_REQUEST
        self.gpu_tokens_per_sec = settings.GPU_INFERENCE_TOKENS_PER_SEC
        self.gpu_memory_gb = settings.GPU_MEMORY_GB

    def estimate_capacity(self, scale_factor: float = 1.0) -> list[CapacityEstimate]:
        baseline = self.baseline_rps * scale_factor
        peak = baseline * self.peak_multiplier
        total_tokens_per_sec = peak * (self.avg_input_tokens + self.avg_output_tokens)

        api_capacity = peak * 2
        api_utilization = (peak / api_capacity) * 100 if api_capacity > 0 else 0

        vector_db_qps = peak * 1.5
        vector_db_capacity = vector_db_qps * 2
        vector_utilization = (vector_db_qps / vector_db_capacity) * 100 if vector_db_capacity > 0 else 0

        gpu_needed = math.ceil(total_tokens_per_sec / self.gpu_tokens_per_sec)
        gpu_capacity = gpu_needed * 2
        gpu_utilization = (gpu_needed / gpu_capacity) * 100 if gpu_capacity > 0 else 0

        queue_capacity = peak * 10
        queue_utilization = (peak / queue_capacity) * 100 if queue_capacity > 0 else 0

        bandwidth_gbps = peak * self.avg_input_tokens * 4 / 1e9
        network_capacity = bandwidth_gbps * 5
        network_utilization = (bandwidth_gbps / network_capacity) * 100 if network_capacity > 0 else 0

        layers = [
            CapacityEstimate(
                layer="API Gateway",
                current_capacity=api_capacity,
                peak_capacity=peak,
                utilization_pct=round(api_utilization, 1),
                bottleneck=api_utilization > 80,
                recommendation="Horizontal scaling with load balancer" if api_utilization > 80 else "Sufficient capacity"
            ),
            CapacityEstimate(
                layer="Vector Database",
                current_capacity=vector_db_capacity,
                peak_capacity=vector_db_qps,
                utilization_pct=round(vector_utilization, 1),
                bottleneck=vector_utilization > 80,
                recommendation="Add read replicas or sharding" if vector_utilization > 80 else "Sufficient capacity"
            ),
            CapacityEstimate(
                layer="GPU Inference",
                current_capacity=gpu_capacity,
                peak_capacity=gpu_needed,
                utilization_pct=round(gpu_utilization, 1),
                bottleneck=gpu_utilization > 80,
                recommendation="Add GPU instances or use model quantization" if gpu_utilization > 80 else "Sufficient capacity"
            ),
            CapacityEstimate(
                layer="Queue",
                current_capacity=queue_capacity,
                peak_capacity=peak,
                utilization_pct=round(queue_utilization, 1),
                bottleneck=queue_utilization > 80,
                recommendation="Increase queue capacity or add consumers" if queue_utilization > 80 else "Sufficient capacity"
            ),
            CapacityEstimate(
                layer="Network",
                current_capacity=round(network_capacity, 2),
                peak_capacity=round(bandwidth_gbps, 2),
                utilization_pct=round(network_utilization, 1),
                bottleneck=network_utilization > 80,
                recommendation="Upgrade network or add CDN" if network_utilization > 80 else "Sufficient capacity"
            ),
        ]

        return layers

    def find_bottleneck(self, scale_factor: float = 1.0) -> CapacityEstimate:
        layers = self.estimate_capacity(scale_factor)
        bottlenecks = [l for l in layers if l.bottleneck]
        if bottlenecks:
            return max(bottlenecks, key=lambda l: l.utilization_pct)
        return min(layers, key=lambda l: l.utilization_pct)

    def create_scale_plan(self, name: str, scale_factor: float = 1.0) -> ScalePlan:
        layers = self.estimate_capacity(scale_factor)
        baseline = self.baseline_rps * scale_factor
        peak = baseline * self.peak_multiplier

        total_tokens_per_sec = peak * (self.avg_input_tokens + self.avg_output_tokens)
        gpu_count = math.ceil(total_tokens_per_sec / self.gpu_tokens_per_sec)
        gpu_monthly = gpu_count * settings.GPU_COST_PER_HOUR * 730

        api_monthly = 200 * scale_factor
        vector_monthly = 500 * scale_factor
        storage_monthly = 100 * scale_factor
        monitoring_monthly = 150 * scale_factor

        total_monthly = gpu_monthly + api_monthly + vector_monthly + storage_monthly + monitoring_monthly

        bottleneck = self.find_bottleneck(scale_factor)

        return ScalePlan(
            id=f"plan-{name.lower().replace(' ', '-')}",
            name=name,
            baseline_requests_per_sec=baseline,
            peak_requests_per_sec=peak,
            layers=layers,
            monthly_cost_estimate=round(total_monthly, 2),
            first_bottleneck=bottleneck.layer
        )

    def compare_plans(self, factors: list[float]) -> list[dict]:
        plans = []
        for f in factors:
            plan = self.create_scale_plan(f"Scale {f}x", f)
            bottleneck = self.find_bottleneck(f)
            plans.append({
                "scale_factor": f,
                "baseline_rps": plan.baseline_requests_per_sec,
                "peak_rps": plan.peak_requests_per_sec,
                "monthly_cost": plan.monthly_cost_estimate,
                "first_bottleneck": bottleneck.layer,
                "gpu_needed": math.ceil(
                    plan.peak_requests_per_sec *
                    (self.avg_input_tokens + self.avg_output_tokens) /
                    self.gpu_tokens_per_sec
                )
            })
        return plans

    def estimate_cost_per_request(self, scale_factor: float = 1.0) -> dict:
        plan = self.create_scale_plan(f"Cost {scale_factor}x", scale_factor)
        monthly_requests = plan.baseline_requests_per_sec * 86400 * 30
        cost_per_req = plan.monthly_cost_estimate / monthly_requests if monthly_requests > 0 else 0

        token_cost_per_req = (
            (self.avg_input_tokens / 1_000_000) * settings.COST_PER_1M_INPUT_TOKENS +
            (self.avg_output_tokens / 1_000_000) * settings.COST_PER_1M_OUTPUT_TOKENS
        )

        return {
            "scale_factor": scale_factor,
            "monthly_requests": int(monthly_requests),
            "total_monthly_cost": plan.monthly_cost_estimate,
            "cost_per_request": round(cost_per_req, 8),
            "token_cost_per_request": round(token_cost_per_req, 6),
            "infrastructure_cost_per_request": round(
                plan.monthly_cost_estimate / monthly_requests - token_cost_per_req, 8
            ) if monthly_requests > 0 else 0
        }
