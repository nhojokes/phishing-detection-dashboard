from typing import Dict, Any

class RiskEngine:
    """Combines modular scores into a final weighted score and classification."""
    
    WEIGHTS = {
        "url": 0.35,
        "sender": 0.25,
        "content": 0.20,
        "ml": 0.20
    }
    
    @classmethod
    def calculate_risk(
        cls, 
        url_res: Dict[str, Any], 
        sender_res: Dict[str, Any], 
        content_res: Dict[str, Any], 
        ml_res: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        composite_score = (
            (url_res["max_url_score"] * cls.WEIGHTS["url"]) +
            (sender_res["risk_score"] * cls.WEIGHTS["sender"]) +
            (content_res["risk_score"] * cls.WEIGHTS["content"]) +
            (ml_res["ml_score"] * cls.WEIGHTS["ml"])
        )
        
        final_score = round(min(composite_score, 100.0), 1)
        
        # Classification Thresholds
        if final_score < 25.0:
            classification = "SAFE"
            severity = "success"
        elif final_score < 50.0:
            classification = "LOW RISK"
            severity = "info"
        elif final_score < 75.0:
            classification = "SUSPICIOUS"
            severity = "warning"
        else:
            classification = "HIGH RISK / LIKELY PHISHING"
            severity = "error"
            
        # Consolidate all explanation points
        explanations = []
        explanations.extend(url_res.get("reasons", []))
        explanations.extend(sender_res.get("reasons", []))
        explanations.extend(content_res.get("reasons", []))
        if ml_res.get("ml_score", 0) > 60:
            explanations.append(f"ML Model detected overall statistical structure matching phishing ({ml_res['ml_score']}% probability).")
            
        if not explanations:
            explanations.append("No alarming threat indicators detected in header, content, or URLs.")

        return {
            "final_score": final_score,
            "classification": classification,
            "severity": severity,
            "explanations": explanations,
            "breakdown": {
                "URL Score": url_res["max_url_score"],
                "Sender Score": sender_res["risk_score"],
                "Content Score": content_res["risk_score"],
                "ML Probability Score": ml_res["ml_score"]
            }
        }