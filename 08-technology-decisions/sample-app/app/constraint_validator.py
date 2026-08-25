"""Constraint Validator — manage hard and soft constraints for technology decisions."""
import uuid
from datetime import datetime
from app.models import HardConstraint, ConstraintType


class ConstraintManager:
    """Manage hard and soft constraints for technology decisions."""

    def __init__(self):
        self._constraints: dict[str, HardConstraint] = {}
        self._seed_constraints()

    def _seed_constraints(self):
        self.add_constraint(
            name="Data Cannot Leave VPC",
            description="Sensitive data (legal, financial, HR) must remain within our VPC. "
                       "Any managed service that sends data externally is disqualified for these workloads.",
            eliminates=["External managed LLM for sensitive data"]
        )

        self.add_constraint(
            name="SOC 2 Compliance Required",
            description="All production systems must meet SOC 2 compliance requirements.",
            eliminates=[]
        )

        self.add_constraint(
            name="Team Can Operate Technology",
            description="The team must have sufficient expertise to operate the technology in production. "
                       "Self-hosted GPU infrastructure requires ML infrastructure engineers.",
            eliminates=["Self-hosted GPU without ML engineers"]
        )

        self.add_constraint(
            name="Budget Limit",
            description="Total monthly AI infrastructure cost must not exceed $15,000.",
            eliminates=[]
        )

        self.add_constraint(
            name="Latency Requirement",
            description="p95 latency must be under 200ms for user-facing queries.",
            eliminates=[]
        )

        self.add_constraint(
            name="No Single Provider Dependency",
            description="Must have fallback capability. No single point of failure for model inference.",
            eliminates=["Single managed provider without fallback"]
        )

        self.add_constraint(
            name="Enterprise IAM Integration",
            description="Must integrate with existing enterprise identity provider (Okta/Azure AD).",
            eliminates=[]
        )

    def add_constraint(self, name: str, description: str,
                       eliminates: list[str] = None,
                       constraint_type: ConstraintType = ConstraintType.HARD) -> HardConstraint:
        constraint_id = f"constraint-{len(self._constraints) + 1:03d}"
        constraint = HardConstraint(
            id=constraint_id,
            name=name,
            description=description,
            constraint_type=constraint_type,
            eliminates_options=eliminates or []
        )
        self._constraints[constraint_id] = constraint
        return constraint

    def validate_option(self, option_name: str,
                        option_description: str = "") -> dict:
        violations = []
        satisfied = []

        for constraint in self._constraints.values():
            if constraint.constraint_type == ConstraintType.HARD:
                is_violated = False

                if option_name in constraint.eliminates_options:
                    is_violated = True
                elif any(keyword in option_description.lower()
                         for keyword in self._get_violation_keywords(constraint.name)):
                    is_violated = True

                if is_violated:
                    violations.append({
                        "constraint_id": constraint.id,
                        "constraint_name": constraint.name,
                        "description": constraint.description
                    })
                else:
                    satisfied.append(constraint.name)

        return {
            "option": option_name,
            "is_valid": len(violations) == 0,
            "violations": violations,
            "satisfied_constraints": satisfied,
            "total_constraints": len(self._constraints)
        }

    def _get_violation_keywords(self, constraint_name: str) -> list[str]:
        keyword_map = {
            "Data Cannot Leave VPC": ["external", "cloud api", "sends data externally"],
            "Team Can Operate Technology": ["gpu infrastructure", "ml infrastructure"],
            "Budget Limit": ["over budget"],
            "Latency Requirement": ["high latency"],
            "No Single Provider Dependency": ["single provider", "no fallback"],
        }
        return keyword_map.get(constraint_name, [])

    def get_all_constraints(self) -> list[HardConstraint]:
        return list(self._constraints.values())

    def get_constraints_summary(self) -> list[dict]:
        return [
            {
                "id": c.id,
                "name": c.name,
                "type": c.constraint_type.value,
                "eliminates_count": len(c.eliminates_options)
            }
            for c in self._constraints.values()
        ]

    def check_all_options(self, options: list[dict]) -> list[dict]:
        results = []
        for opt in options:
            result = self.validate_option(
                option_name=opt.get("name", ""),
                option_description=opt.get("description", "")
            )
            results.append(result)
        return results
