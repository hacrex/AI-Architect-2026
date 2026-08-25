"""Data Classifier — PII detection, classification, and redaction."""
import re
from app.models import PIIDetection, DataClassification, ClassificationLevel
import config.settings as settings


class DataClassifier:
    """Detect PII and classify data sensitivity."""

    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[-.\s]?\d{4}[-.\s]?\d{4}[-.\s]?\d{4}\b')
    NAME_KEYWORDS = ["name", "employee", "customer", "patient", "applicant"]
    SALARY_KEYWORDS = ["salary", "compensation", "pay", "wage", "earnings"]
    MEDICAL_KEYWORDS = ["diagnosis", "patient", "medical", "health", "treatment", "condition"]
    FINANCIAL_KEYWORDS = ["account number", "routing number", "balance", "transaction"]

    def __init__(self):
        self._scan_count = 0
        self._pii_count = 0
        self._redaction_count = 0

    def detect_pii(self, text: str) -> PIIDetection:
        self._scan_count += 1
        detections = []
        redacted = text

        emails = self.EMAIL_PATTERN.findall(text)
        for email in emails:
            detections.append({"type": "email", "value": email, "start": text.find(email)})
            redacted = redacted.replace(email, self._mask_email(email))

        phones = self.PHONE_PATTERN.findall(text)
        for phone in phones:
            detections.append({"type": "phone", "value": phone, "start": text.find(phone)})
            redacted = redacted.replace(phone, self._mask_phone(phone))

        ssns = self.SSN_PATTERN.findall(text)
        for ssn in ssns:
            detections.append({"type": "ssn", "value": ssn, "start": text.find(ssn)})
            redacted = redacted.replace(ssn, "[SSN-REDACTED]")

        cards = self.CREDIT_CARD_PATTERN.findall(text)
        for card in cards:
            detections.append({"type": "credit_card", "value": card, "start": text.find(card)})
            redacted = redacted.replace(card, "[CARD-REDACTED]")

        has_pii = len(detections) > 0
        if has_pii:
            self._pii_count += 1
            self._redaction_count += 1

        pii_types = list(set(d["type"] for d in detections))
        classification = self._classify_text(text, pii_types)

        return PIIDetection(
            text=text[:500],
            has_pii=has_pii,
            pii_types=pii_types,
            detections=detections,
            redacted_text=redacted,
            classification=classification
        )

    def classify(self, content: str) -> DataClassification:
        indicators = []
        classification = ClassificationLevel.PUBLIC

        lower = content.lower()

        if any(kw in lower for kw in self.MEDICAL_KEYWORDS):
            classification = ClassificationLevel.RESTRICTED
            indicators.append("medical_content")

        if any(kw in lower for kw in self.SALARY_KEYWORDS):
            classification = ClassificationLevel.CONFIDENTIAL
            indicators.append("salary_content")

        if any(kw in lower for kw in self.FINANCIAL_KEYWORDS):
            classification = ClassificationLevel.CONFIDENTIAL
            indicators.append("financial_content")

        if self.EMAIL_PATTERN.search(content) or self.PHONE_PATTERN.search(content):
            if classification == ClassificationLevel.PUBLIC:
                classification = ClassificationLevel.INTERNAL
            indicators.append("pii_detected")

        if self.SSN_PATTERN.search(content):
            classification = ClassificationLevel.RESTRICTED
            indicators.append("ssn_detected")

        if any(kw in lower for kw in ["confidential", "secret", "private", "restricted"]):
            if classification.value < ClassificationLevel.CONFIDENTIAL.value:
                classification = ClassificationLevel.CONFIDENTIAL
            indicators.append("explicit_classification")

        confidence = 0.5
        if indicators:
            confidence = min(0.95, 0.5 + len(indicators) * 0.15)

        return DataClassification(
            content=content[:200],
            classification=classification,
            confidence=confidence,
            indicators=indicators
        )

    def _classify_text(self, text: str, pii_types: list[str]) -> ClassificationLevel:
        if "ssn" in pii_types or "credit_card" in pii_types:
            return ClassificationLevel.RESTRICTED
        if "email" in pii_types or "phone" in pii_types:
            return ClassificationLevel.CONFIDENTIAL
        return ClassificationLevel.INTERNAL

    def _mask_email(self, email: str) -> str:
        parts = email.split("@")
        if len(parts) == 2:
            masked_name = parts[0][0] + "***"
            return f"{masked_name}@***.com"
        return "[EMAIL-REDACTED]"

    def _mask_phone(self, phone: str) -> str:
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            return f"+XX XXXXX {digits[-4:]}"
        return "[PHONE-REDACTED]"

    def get_stats(self) -> dict:
        return {
            "total_scans": self._scan_count,
            "pii_detected": self._pii_count,
            "redactions_performed": self._redaction_count,
            "pii_rate_pct": round(
                self._pii_count / self._scan_count * 100, 1
            ) if self._scan_count > 0 else 0
        }
