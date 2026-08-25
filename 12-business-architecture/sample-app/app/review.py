"""Architecture Review — structured review and checklist."""
from datetime import datetime
from typing import Optional
from app.models import ArchitectureReview, ReviewSection, ArchitecturePhase
import config.settings as settings


class ReviewManager:
    """Manage architecture reviews and checklists."""

    def __init__(self):
        self._reviews: dict[str, ArchitectureReview] = {}
        self._seed_reviews()

    def _seed_reviews(self):
        sections = [
            ReviewSection(phase=ArchitecturePhase.PROBLEM, question="What problem are we solving?", time_minutes=5),
            ReviewSection(phase=ArchitecturePhase.OUTCOME, question="Who benefits and how will we measure success?", time_minutes=3),
            ReviewSection(phase=ArchitecturePhase.REQUIREMENTS, question="What must the system achieve?", time_minutes=5),
            ReviewSection(phase=ArchitecturePhase.ARCHITECTURE, question="What are the major components?", time_minutes=10),
            ReviewSection(phase=ArchitecturePhase.DECISIONS, question="What are the top 3 choices?", time_minutes=5),
            ReviewSection(phase=ArchitecturePhase.RISKS, question="What could go wrong?", time_minutes=5),
            ReviewSection(phase=ArchitecturePhase.COST, question="What is the expected operating model?", time_minutes=5),
            ReviewSection(phase=ArchitecturePhase.SUCCESS, question="How will we know it worked?", time_minutes=5),
        ]

        self.create_review(ArchitectureReview(
            project_id="proj-001",
            project_name="Enterprise AI Knowledge Platform",
            sections=sections,
            total_time_minutes=45
        ))

    def create_review(self, review: ArchitectureReview) -> ArchitectureReview:
        key = f"{review.project_id}"
        self._reviews[key] = review
        return review

    def get_review(self, project_id: str) -> Optional[ArchitectureReview]:
        return self._reviews.get(project_id)

    def list_reviews(self) -> list[ArchitectureReview]:
        return list(self._reviews.values())

    def answer_question(self, project_id: str, phase: ArchitecturePhase, answer: str) -> Optional[ArchitectureReview]:
        review = self._reviews.get(project_id)
        if not review:
            return None
        for section in review.sections:
            if section.phase == phase:
                section.answer = answer
                return review
        return None

    def get_checklist(self) -> list[dict]:
        questions = [
            ("Business", "What problem are we solving?"),
            ("Users", "Who benefits?"),
            ("Value", "How will we measure success?"),
            ("Data", "Where does the information come from?"),
            ("AI", "Why does AI need to be involved?"),
            ("Architecture", "Why are these components necessary?"),
            ("Technology", "Why these technologies?"),
            ("Scale", "What happens at 10x traffic?"),
            ("Reliability", "What happens when dependencies fail?"),
            ("Security", "What can users and agents access?"),
            ("Governance", "Who owns the system?"),
            ("Cost", "What will it cost to operate?"),
            ("Observability", "How will we know when it is failing?"),
            ("Change", "What happens when models and requirements change?"),
        ]
        return [{"area": area, "question": q} for area, q in questions]

    def get_summary(self) -> dict:
        reviews = list(self._reviews.values())
        total_sections = sum(len(r.sections) for r in reviews)
        answered = sum(
            1 for r in reviews
            for s in r.sections
            if s.answer
        )
        return {
            "total_reviews": len(reviews),
            "total_sections": total_sections,
            "answered_sections": answered,
            "completion_pct": round(answered / total_sections * 100, 1) if total_sections > 0 else 0,
            "reviews": [
                {"project": r.project_name, "sections": len(r.sections),
                 "answered": sum(1 for s in r.sections if s.answer)}
                for r in reviews
            ]
        }

    def format_review(self, project_id: str) -> str:
        review = self._reviews.get(project_id)
        if not review:
            return f"Review for {project_id} not found"
        lines = [
            f"# Architecture Review: {review.project_name}",
            "",
            f"**Total Time:** {review.total_time_minutes} minutes",
            "",
        ]
        for section in review.sections:
            answer_display = section.answer if section.answer else "[Not answered]"
            lines.extend([
                f"## {section.phase.value.title()} ({section.time_minutes} min)",
                f"**Question:** {section.question}",
                f"**Answer:** {answer_display}",
                "",
            ])
        return "\n".join(lines)
