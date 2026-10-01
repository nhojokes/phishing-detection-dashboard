import re
from typing import Dict, Any

class ContentAnalyzer:
    """Analyzes email text for psychological social engineering drivers."""
    
    URGENCY_KEYWORDS = [
        "urgent", "immediately", "action required", "account suspended", 
        "24 hours", "unauthorized access", "expire today", "terminated", "final notice"
    ]
    
    FINANCIAL_KEYWORDS = [
        "invoice", "wire transfer", "payment overdue", "tax refund", 
        "gift card", "crypto", "direct deposit", "payroll", "claim reward", "$10,000"
    ]
    
    FEAR_KEYWORDS = [
        "legal action", "police", "arrest", "breach", "security threat", 
        "unauthorized transaction", "penalty", "court"
    ]

    @classmethod
    def analyze(cls, subject: str, body: str) -> Dict[str, Any]:
        full_text = f"{subject} {body}".lower()
        score = 0
        reasons = []
        
        urgency_matches = [w for w in cls.URGENCY_KEYWORDS if w in full_text]
        financial_matches = [w for w in cls.FINANCIAL_KEYWORDS if w in full_text]
        fear_matches = [w for w in cls.FEAR_KEYWORDS if w in full_text]
        
        if urgency_matches:
            score += len(urgency_matches) * 10
            reasons.append(f"Urgency / Time Pressure language detected: {', '.join(urgency_matches)}")
            
        if financial_matches:
            score += len(financial_matches) * 10
            reasons.append(f"Financial / Monetary lure detected: {', '.join(financial_matches)}")
            
        if fear_matches:
            score += len(fear_matches) * 15
            reasons.append(f"Fear / Coercive pressure tactics detected: {', '.join(fear_matches)}")
            
        # Check for ALL CAPS in Subject
        if subject.isupper() and len(subject) > 5:
            score += 10
            reasons.append("Subject line uses ALL CAPS to induce stress.")
            
        return {
            "urgency_count": len(urgency_matches),
            "financial_count": len(financial_matches),
            "fear_count": len(fear_matches),
            "risk_score": min(score, 100),
            "reasons": reasons
        }