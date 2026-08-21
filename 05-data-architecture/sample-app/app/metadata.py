"""Metadata extraction for documents."""
import re
from datetime import datetime
from typing import Optional


DEPARTMENT_KEYWORDS = {
    "engineering": [
        "kubernetes", "docker", "deploy", "ci/cd", "pipeline", "code",
        "api", "database", "server", "infrastructure", "cloud", "aws",
        "azure", "gcp", "microservices", "container", "yaml", "terraform"
    ],
    "hr": [
        "leave", "vacation", "holiday", "benefits", "onboarding",
        "performance", "review", "compensation", "hiring", "policy",
        "employee", "workforce", "training", "development"
    ],
    "security": [
        "security", "compliance", "audit", "encryption", "firewall",
        "access", "authentication", "authorization", "vulnerability",
        "incident", "response", "data protection", "gdpr", "soc2"
    ],
    "finance": [
        "budget", "cost", "revenue", "expense", "invoice", "payment",
        "financial", "quarterly", "annual", "forecast", "variance"
    ],
    "legal": [
        "contract", "agreement", "terms", "conditions", "liability",
        "intellectual property", "patent", "trademark", "regulation"
    ],
}

CLASSIFICATION_KEYWORDS = {
    "restricted": [
        "top secret", "confidential", "restricted", "do not distribute",
        "need to know", "classified"
    ],
    "confidential": [
        "confidential", "internal only", "sensitive", "private",
        "not for public", "do not share"
    ],
    "internal": [
        "internal", "company", "employee", "staff", "team"
    ],
    "public": [
        "public", "external", "customer", "partner", "vendor"
    ],
}


def extract_department(text: str, title: str = "") -> str:
    """
    Extract department from document content and title.
    
    Args:
        text: Document content
        title: Document title
        
    Returns:
        Department name
    """
    combined = (title + " " + text).lower()
    
    scores = {}
    for dept, keywords in DEPARTMENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        scores[dept] = score
    
    if max(scores.values()) == 0:
        return "engineering"
    
    return max(scores, key=scores.get)


def extract_classification(text: str, title: str = "") -> str:
    """
    Extract document classification from content and title.
    
    Args:
        text: Document content
        title: Document title
        
    Returns:
        Classification level
    """
    combined = (title + " " + text).lower()
    
    for level in ["restricted", "confidential", "internal", "public"]:
        keywords = CLASSIFICATION_KEYWORDS[level]
        if any(kw in combined for kw in keywords):
            return level
    
    return "internal"


def extract_version(text: str) -> int:
    """
    Extract document version from content.
    
    Args:
        text: Document content
        
    Returns:
        Version number
    """
    version_patterns = [
        r'version\s+(\d+)',
        r'v(\d+)',
        r'revision\s+(\d+)',
        r'(\d+)\.\d+\.\d+',
    ]
    
    for pattern in version_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return 1


def extract_dates(text: str) -> dict:
    """
    Extract dates from document content.
    
    Args:
        text: Document content
        
    Returns:
        Dictionary with created and updated dates
    """
    date_patterns = [
        r'created:\s*(\d{4}-\d{2}-\d{2})',
        r'updated:\s*(\d{4}-\d{2}-\d{2})',
        r'last modified:\s*(\d{4}-\d{2}-\d{2})',
        r'effective date:\s*(\d{4}-\d{2}-\d{2})',
    ]
    
    dates = {}
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            if "created" in pattern:
                dates["created"] = date_str
            elif "updated" in pattern or "modified" in pattern:
                dates["updated"] = date_str
            elif "effective" in pattern:
                dates["effective"] = date_str
    
    return dates


def extract_metadata(
    document_id: str,
    title: str,
    content: str,
    department: Optional[str] = None,
    classification: Optional[str] = None,
    owner: Optional[str] = None,
) -> dict:
    """
    Extract all metadata from a document.
    
    Args:
        document_id: Document identifier
        title: Document title
        content: Document content
        department: Override department (auto-detect if None)
        classification: Override classification (auto-detect if None)
        owner: Document owner
        
    Returns:
        Metadata dictionary
    """
    detected_dept = extract_department(content, title)
    detected_class = extract_classification(content, title)
    version = extract_version(content)
    dates = extract_dates(content)
    
    return {
        "document_id": document_id,
        "title": title,
        "department": department or detected_dept,
        "classification": classification or detected_class,
        "owner": owner or f"{department or detected_dept}-team",
        "version": version,
        "created_at": dates.get("created", datetime.now().strftime("%Y-%m-%d")),
        "updated_at": dates.get("updated", datetime.now().strftime("%Y-%m-%d")),
        "word_count": len(content.split()),
        "char_count": len(content),
    }
