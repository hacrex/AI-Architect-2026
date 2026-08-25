"""Decision Engine — technology selection with weighted scoring and hard constraints."""
import uuid
from datetime import datetime
from app.models import (
    DecisionMatrix, DecisionCriteria, TechnologyOption, OptionScore,
    TechnologyCategory, HardConstraint, ConstraintType
)


class ConstraintValidator:
    """Validate options against hard constraints."""

    def __init__(self):
        self._constraints: list[HardConstraint] = []

    def add_constraint(self, name: str, description: str,
                       eliminates: list[str] = None) -> HardConstraint:
        constraint = HardConstraint(
            id=f"constraint-{len(self._constraints) + 1:03d}",
            name=name,
            description=description,
            eliminates_options=eliminates or []
        )
        self._constraints.append(constraint)
        return constraint

    def validate(self, option_name: str) -> list[HardConstraint]:
        violations = []
        for c in self._constraints:
            if c.constraint_type == ConstraintType.HARD:
                if option_name in c.eliminates_options:
                    c.is_satisfied = False
                    violations.append(c)
                else:
                    c.is_satisfied = True
        return violations

    def get_all_constraints(self) -> list[HardConstraint]:
        return self._constraints

    def get_violations(self, option_name: str) -> list[str]:
        violations = self.validate(option_name)
        return [v.name for v in violations]


class WeightedScorer:
    """Calculate weighted scores for technology options."""

    def calculate_weighted_score(self, scores: dict[str, float],
                                  criteria: list[DecisionCriteria]) -> float:
        total = 0.0
        total_weight = 0.0

        for c in criteria:
            if c.name in scores:
                total += scores[c.name] * c.weight
                total_weight += c.weight

        if total_weight > 0:
            return round(total / total_weight, 4)
        return 0.0

    def rank_options(self, option_scores: list[OptionScore]) -> list[OptionScore]:
        valid = [s for s in option_scores if not s.is_disqualified]
        invalid = [s for s in option_scores if s.is_disqualified]
        valid.sort(key=lambda s: s.weighted_score, reverse=True)
        return valid + invalid


class DecisionEngine:
    """Complete technology decision engine."""

    def __init__(self):
        self.constraint_validator = ConstraintValidator()
        self.scorer = WeightedScorer()
        self._matrices: dict[str, DecisionMatrix] = {}
        self._seed_default_constraints()
        self._seed_sample_matrices()

    def _seed_default_constraints(self):
        self.constraint_validator.add_constraint(
            name="data_privacy",
            description="Sensitive data must remain within our environment",
            eliminates=[]
        )
        self.constraint_validator.add_constraint(
            name="team_capability",
            description="Team must be able to operate the technology",
            eliminates=[]
        )
        self.constraint_validator.add_constraint(
            name="budget",
            description="Monthly cost must be within allocated budget",
            eliminates=[]
        )

    def _seed_sample_matrices(self):
        self.create_model_hosting_matrix()
        self.create_vector_storage_matrix()
        self.create_inference_platform_matrix()

    def create_model_hosting_matrix(self) -> DecisionMatrix:
        criteria = [
            DecisionCriteria(name="capability", weight=0.20, description="Functional capability"),
            DecisionCriteria(name="cost_at_scale", weight=0.20, description="Cost at projected volume"),
            DecisionCriteria(name="data_privacy", weight=0.20, description="Data privacy compliance"),
            DecisionCriteria(name="latency", weight=0.10, description="Response latency"),
            DecisionCriteria(name="team_capability", weight=0.10, description="Team can operate it"),
            DecisionCriteria(name="vendor_independence", weight=0.10, description="Reduced lock-in"),
            DecisionCriteria(name="maintenance", weight=0.10, description="Ongoing maintenance burden"),
        ]

        options = [
            TechnologyOption(
                name="Managed (OpenAI/Anthropic)",
                category=TechnologyCategory.MODEL_HOSTING,
                description="Managed proprietary LLM API",
                is_managed=True,
                estimated_monthly_cost=2000.0,
                team_expertise_required=2,
                operational_burden=2
            ),
            TechnologyOption(
                name="Self-Hosted (Llama/Mistral)",
                category=TechnologyCategory.MODEL_HOSTING,
                description="Self-hosted open-weight models on GPU",
                is_open_source=True,
                estimated_monthly_cost=8000.0,
                team_expertise_required=8,
                operational_burden=8
            ),
            TechnologyOption(
                name="Hybrid",
                category=TechnologyCategory.MODEL_HOSTING,
                description="Managed for general, self-hosted for sensitive",
                estimated_monthly_cost=5000.0,
                team_expertise_required=5,
                operational_burden=5
            ),
        ]

        scores = [
            OptionScore(
                option_name="Managed (OpenAI/Anthropic)",
                scores={"capability": 9, "cost_at_scale": 7, "data_privacy": 5,
                        "latency": 8, "team_capability": 9, "vendor_independence": 4, "maintenance": 9}
            ),
            OptionScore(
                option_name="Self-Hosted (Llama/Mistral)",
                scores={"capability": 7, "cost_at_scale": 8, "data_privacy": 9,
                        "latency": 9, "team_capability": 4, "vendor_independence": 9, "maintenance": 3}
            ),
            OptionScore(
                option_name="Hybrid",
                scores={"capability": 8, "cost_at_scale": 7, "data_privacy": 7,
                        "latency": 8, "team_capability": 6, "vendor_independence": 7, "maintenance": 5}
            ),
        ]

        for s in scores:
            violations = self.constraint_validator.get_violations(s.option_name)
            s.hard_constraint_violations = violations
            s.is_disqualified = len(violations) > 0
            s.weighted_score = self.scorer.calculate_weighted_score(s.scores, criteria)

        ranked = self.scorer.rank_options(scores)
        selected = ranked[0].option_name if ranked and not ranked[0].is_disqualified else None

        matrix = DecisionMatrix(
            id="matrix-001",
            category=TechnologyCategory.MODEL_HOSTING,
            title="Model Hosting Strategy",
            criteria=criteria,
            options=options,
            scores=ranked,
            hard_constraints=["data_privacy", "team_capability"],
            selected_option=selected,
            rationale="Hybrid allows routing sensitive workloads to self-hosted while leveraging managed for general tasks."
        )
        self._matrices[matrix.id] = matrix
        return matrix

    def create_vector_storage_matrix(self) -> DecisionMatrix:
        criteria = [
            DecisionCriteria(name="capability", weight=0.20),
            DecisionCriteria(name="cost_at_scale", weight=0.20),
            DecisionCriteria(name="operational_burden", weight=0.20),
            DecisionCriteria(name="scalability", weight=0.15),
            DecisionCriteria(name="team_capability", weight=0.15),
            DecisionCriteria(name="vendor_lock_in", weight=0.10),
        ]

        options = [
            TechnologyOption(name="PostgreSQL + pgvector", category=TechnologyCategory.VECTOR_STORAGE,
                             description="Use existing PostgreSQL with pgvector extension",
                             estimated_monthly_cost=500.0, team_expertise_required=3, operational_burden=3),
            TechnologyOption(name="Dedicated Vector DB (Pinecone)", category=TechnologyCategory.VECTOR_STORAGE,
                             description="Managed vector database service",
                             is_managed=True, estimated_monthly_cost=1500.0, team_expertise_required=2, operational_burden=2),
            TechnologyOption(name="Managed Vector Service (Weaviate Cloud)", category=TechnologyCategory.VECTOR_STORAGE,
                             description="Managed vector database with advanced features",
                             is_managed=True, estimated_monthly_cost=2000.0, team_expertise_required=2, operational_burden=2),
        ]

        scores = [
            OptionScore(option_name="PostgreSQL + pgvector",
                        scores={"capability": 7, "cost_at_scale": 9, "operational_burden": 7,
                                "scalability": 6, "team_capability": 8, "vendor_lock_in": 9}),
            OptionScore(option_name="Dedicated Vector DB (Pinecone)",
                        scores={"capability": 9, "cost_at_scale": 6, "operational_burden": 9,
                                "scalability": 9, "team_capability": 8, "vendor_lock_in": 4}),
            OptionScore(option_name="Managed Vector Service (Weaviate Cloud)",
                        scores={"capability": 8, "cost_at_scale": 5, "operational_burden": 9,
                                "scalability": 8, "team_capability": 8, "vendor_lock_in": 5}),
        ]

        for s in scores:
            violations = self.constraint_validator.get_violations(s.option_name)
            s.hard_constraint_violations = violations
            s.is_disqualified = len(violations) > 0
            s.weighted_score = self.scorer.calculate_weighted_score(s.scores, criteria)

        ranked = self.scorer.rank_options(scores)
        selected = ranked[0].option_name if ranked and not ranked[0].is_disqualified else None

        matrix = DecisionMatrix(
            id="matrix-002",
            category=TechnologyCategory.VECTOR_STORAGE,
            title="Vector Storage Strategy",
            criteria=criteria,
            options=options,
            scores=ranked,
            selected_option=selected,
            rationale="PostgreSQL + pgvector leverages existing infrastructure and team knowledge."
        )
        self._matrices[matrix.id] = matrix
        return matrix

    def create_inference_platform_matrix(self) -> DecisionMatrix:
        criteria = [
            DecisionCriteria(name="capability", weight=0.20),
            DecisionCriteria(name="cost_at_scale", weight=0.20),
            DecisionCriteria(name="latency", weight=0.15),
            DecisionCriteria(name="scalability", weight=0.15),
            DecisionCriteria(name="team_capability", weight=0.15),
            DecisionCriteria(name="maintenance", weight=0.15),
        ]

        options = [
            TechnologyOption(name="Managed API (OpenAI)", category=TechnologyCategory.INFERENCE_PLATFORM,
                             description="Direct API calls to managed providers",
                             is_managed=True, estimated_monthly_cost=2000.0, team_expertise_required=2, operational_burden=2),
            TechnologyOption(name="vLLM on Kubernetes", category=TechnologyCategory.INFERENCE_PLATFORM,
                             description="Self-hosted inference with vLLM on K8s",
                             is_open_source=True, estimated_monthly_cost=8000.0, team_expertise_required=7, operational_burden=7),
            TechnologyOption(name="KServe", category=TechnologyCategory.INFERENCE_PLATFORM,
                             description="Kubernetes-native model serving",
                             is_open_source=True, estimated_monthly_cost=6000.0, team_expertise_required=6, operational_burden=5),
            TechnologyOption(name="Hybrid (Managed + vLLM)", category=TechnologyCategory.INFERENCE_PLATFORM,
                             description="Managed for general, self-hosted for sensitive",
                             estimated_monthly_cost=5000.0, team_expertise_required=5, operational_burden=5),
        ]

        scores = [
            OptionScore(option_name="Managed API (OpenAI)",
                        scores={"capability": 9, "cost_at_scale": 6, "latency": 7,
                                "scalability": 8, "team_capability": 9, "maintenance": 9}),
            OptionScore(option_name="vLLM on Kubernetes",
                        scores={"capability": 8, "cost_at_scale": 8, "latency": 9,
                                "scalability": 8, "team_capability": 4, "maintenance": 4}),
            OptionScore(option_name="KServe",
                        scores={"capability": 8, "cost_at_scale": 7, "latency": 8,
                                "scalability": 9, "team_capability": 5, "maintenance": 5}),
            OptionScore(option_name="Hybrid (Managed + vLLM)",
                        scores={"capability": 8, "cost_at_scale": 7, "latency": 8,
                                "scalability": 8, "team_capability": 6, "maintenance": 5}),
        ]

        for s in scores:
            violations = self.constraint_validator.get_violations(s.option_name)
            s.hard_constraint_violations = violations
            s.is_disqualified = len(violations) > 0
            s.weighted_score = self.scorer.calculate_weighted_score(s.scores, criteria)

        ranked = self.scorer.rank_options(scores)
        selected = ranked[0].option_name if ranked and not ranked[0].is_disqualified else None

        matrix = DecisionMatrix(
            id="matrix-003",
            category=TechnologyCategory.INFERENCE_PLATFORM,
            title="Inference Platform Strategy",
            criteria=criteria,
            options=options,
            scores=ranked,
            selected_option=selected,
            rationale="Hybrid balances managed simplicity for general workloads with self-hosted control for sensitive data."
        )
        self._matrices[matrix.id] = matrix
        return matrix

    def create_matrix(self, title: str, category: TechnologyCategory,
                       criteria: list[DecisionCriteria],
                       options: list[TechnologyOption]) -> DecisionMatrix:
        matrix_id = f"matrix-{len(self._matrices) + 1:03d}"
        matrix = DecisionMatrix(
            id=matrix_id,
            category=category,
            title=title,
            criteria=criteria,
            options=options
        )
        self._matrices[matrix_id] = matrix
        return matrix

    def score_option(self, matrix_id: str, option_name: str,
                      scores: dict[str, float]) -> OptionScore:
        matrix = self._matrices.get(matrix_id)
        if not matrix:
            raise ValueError(f"Matrix {matrix_id} not found")

        option_score = OptionScore(
            option_name=option_name,
            scores=scores
        )

        violations = self.constraint_validator.get_violations(option_name)
        option_score.hard_constraint_violations = violations
        option_score.is_disqualified = len(violations) > 0
        option_score.weighted_score = self.scorer.calculate_weighted_score(scores, matrix.criteria)

        existing = [i for i, s in enumerate(matrix.scores) if s.option_name == option_name]
        if existing:
            matrix.scores[existing[0]] = option_score
        else:
            matrix.scores.append(option_score)

        return option_score

    def select_option(self, matrix_id: str) -> str:
        matrix = self._matrices.get(matrix_id)
        if not matrix:
            raise ValueError(f"Matrix {matrix_id} not found")

        ranked = self.scorer.rank_options(matrix.scores)
        matrix.scores = ranked

        if ranked and not ranked[0].is_disqualified:
            matrix.selected_option = ranked[0].option_name
            return ranked[0].option_name
        return None

    def get_matrix(self, matrix_id: str) -> DecisionMatrix:
        return self._matrices.get(matrix_id)

    def list_matrices(self) -> list[DecisionMatrix]:
        return list(self._matrices.values())

    def get_summary(self) -> list[dict]:
        return [
            {
                "id": m.id,
                "title": m.title,
                "category": m.category.value,
                "options_count": len(m.options),
                "scores_count": len(m.scores),
                "selected": m.selected_option
            }
            for m in self._matrices.values()
        ]
