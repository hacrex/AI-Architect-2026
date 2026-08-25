"""Business Metrics — measure AI business value and outcomes."""
from typing import Optional
from app.models import BusinessMetric, BusinessValue, BusinessValue
import config.settings as settings


class BusinessMetricsManager:
    """Track and calculate AI business metrics and value."""

    def __init__(self):
        self._business_values: dict[str, BusinessValue] = {}
        self._seed_values()

    def _seed_values(self):
        self.create_business_value(BusinessValue(
            id="bv-001",
            name="Enterprise Knowledge Platform Value",
            employees_affected=10000,
            time_saved_minutes_per_day=20,
            working_days_per_year=220,
            hourly_rate=60.0,
            metrics=[
                BusinessMetric(name="Resolution Time", category="efficiency",
                              baseline=20.0, target=10.0, unit="minutes",
                              measurement_method="End-to-end task timing"),
                BusinessMetric(name="Task Success Rate", category="quality",
                              baseline=65.0, target=85.0, unit="%",
                              measurement_method="Tasks completed without human"),
                BusinessMetric(name="User Adoption", category="adoption",
                              baseline=0.0, target=70.0, unit="%",
                              measurement_method="Active users / total users"),
                BusinessMetric(name="Human Escalation Rate", category="efficiency",
                              baseline=100.0, target=30.0, unit="%",
                              measurement_method="Transfers to human agent"),
                BusinessMetric(name="Cost per Task", category="cost",
                              baseline=8.50, target=2.00, unit="USD",
                              measurement_method="Total cost / successful tasks"),
            ],
            cost_model_id="cost-001"
        ))

        self.create_business_value(BusinessValue(
            id="bv-002",
            name="AI Inference Platform Value",
            employees_affected=200,
            time_saved_minutes_per_day=30,
            working_days_per_year=220,
            hourly_rate=75.0,
            metrics=[
                BusinessMetric(name="Model Deployment Time", category="efficiency",
                              baseline=5.0, target=0.5, unit="days",
                              measurement_method="Time from request to production"),
                BusinessMetric(name="GPU Utilization", category="cost",
                              baseline=35.0, target=75.0, unit="%",
                              measurement_method="Active GPU hours / available"),
                BusinessMetric(name="Cost per Inference", category="cost",
                              baseline=0.15, target=0.05, unit="USD",
                              measurement_method="Total cost / total inferences"),
            ],
            cost_model_id="cost-002"
        ))

        self.create_business_value(BusinessValue(
            id="bv-003",
            name="Agent Platform Value",
            employees_affected=500,
            time_saved_minutes_per_day=15,
            working_days_per_year=220,
            hourly_rate=65.0,
            metrics=[
                BusinessMetric(name="Agent Task Completion", category="quality",
                              baseline=0.0, target=80.0, unit="%",
                              measurement_method="Tasks completed autonomously"),
                BusinessMetric(name="Cost per Agent Action", category="cost",
                              baseline=0.50, target=0.10, unit="USD",
                              measurement_method="Total cost / agent actions"),
                BusinessMetric(name="Security Incidents", category="security",
                              baseline=5.0, target=0.0, unit="incidents/quarter",
                              measurement_method="Security event count"),
            ],
            cost_model_id="cost-003"
        ))

    def create_business_value(self, bv: BusinessValue) -> BusinessValue:
        self._business_values[bv.id] = bv
        return bv

    def get_business_value(self, bv_id: str) -> Optional[BusinessValue]:
        return self._business_values.get(bv_id)

    def list_business_values(self) -> list[BusinessValue]:
        return list(self._business_values.values())

    def calculate_productivity(self, employees: int, minutes_per_day: float,
                                hourly_rate: float, working_days: int = 220) -> dict:
        hours_per_year = (minutes_per_day / 60) * working_days
        annual_value = employees * hours_per_year * hourly_rate
        monthly_value = annual_value / 12
        daily_value = annual_value / working_days

        return {
            "employees": employees,
            "minutes_per_day": minutes_per_day,
            "hours_per_year": round(hours_per_year, 1),
            "annual_value": round(annual_value, 2),
            "monthly_value": round(monthly_value, 2),
            "daily_value": round(daily_value, 2),
            "hourly_rate": hourly_rate,
        }

    def get_value_summary(self, bv_id: str) -> dict:
        bv = self._business_values.get(bv_id)
        if not bv:
            return {"error": "Business value not found"}

        from app.cost_model import CostManager
        cost_mgr = CostManager()
        cost_model = cost_mgr.get_cost_model(bv.cost_model_id)
        total_cost = cost_model.total_cost() if cost_model else 0

        return {
            "name": bv.name,
            "employees_affected": bv.employees_affected,
            "time_saved_minutes_per_day": bv.time_saved_minutes_per_day,
            "annual_productivity_value": bv.annual_productivity_value(),
            "total_ai_cost": total_cost,
            "roi_pct": bv.roi(total_cost),
            "payback_months": bv.payback_months(total_cost),
            "metrics": [
                {"name": m.name, "category": m.category,
                 "baseline": m.baseline, "target": m.target, "unit": m.unit}
                for m in bv.metrics
            ]
        }

    def get_summary(self) -> dict:
        values = list(self._business_values.values())
        return {
            "total_business_values": len(values),
            "total_employees_affected": sum(v.employees_affected for v in values),
            "total_annual_value": round(sum(v.annual_productivity_value() for v in values), 2),
            "values": [
                {"id": v.id, "name": v.name,
                 "employees": v.employees_affected,
                 "annual_value": v.annual_productivity_value(),
                 "metrics_count": len(v.metrics)}
                for v in values
            ]
        }
