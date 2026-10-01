import re
from typing import Dict, Any

class SenderAnalyzer:
    """Analyzes email sender addresses and domain structures for spoofing markers."""
    
    FREE_PROVIDERS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"}
    POPULAR_BRANDS = ["paypal", "microsoft", "amazon", "apple", "google", "bankofamerica", "wellsfargo", "netflix"]
    
    @classmethod
    def analyze(cls, sender: str) -> Dict[str, Any]:
        score = 0
        reasons = []
        
        # Extract email address
        match = re.search(r'<([^>]+)>', sender)
        email_addr = match.group(1) if match else sender.strip()
        
        if "@" not in email_addr:
            return {
                "sender": sender,
                "risk_score": 50,
                "reasons": ["Malformed email address structure."]
            }
            
        user, domain = email_addr.lower().split("@", 1)
        
        # Typosquatting / Brand impersonation in domain
        for brand in cls.POPULAR_BRANDS:
            if brand in domain and domain not in [f"{brand}.com", f"support.{brand}.com"]:
                score += 40
                reasons.append(f"Potential brand impersonation: Domain '{domain}' contains brand name reference '{brand}'.")
                break
                
        # Lookalike patterns (hyphens, numbers replacing letters)
        if "-" in domain:
            score += 15
            reasons.append("Sender domain contains suspicious hyphens.")
        if re.search(r'\d', domain):
            score += 15
            reasons.append("Sender domain contains numeric substitutions.")
            
        # Display Name Mismatch / Executive Impersonation
        display_name = sender.split("<")[0].strip() if "<" in sender else ""
        if display_name:
            for brand in cls.POPULAR_BRANDS:
                if brand in display_name.lower() and domain in cls.FREE_PROVIDERS:
                    score += 35
                    reasons.append(f"Executive/Brand display name '{display_name}' sent from free email provider '{domain}'.")
                    break
                    
        return {
            "sender": sender,
            "domain": domain,
            "risk_score": min(score, 100),
            "reasons": list(set(reasons))
        }