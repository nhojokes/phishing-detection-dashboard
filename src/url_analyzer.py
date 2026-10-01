import re
from urllib.parse import urlparse
from typing import List, Dict, Any

class URLAnalyzer:
    """Analyzes URLs extracted from email bodies for threat indicators."""
    
    SUSPICIOUS_TLDS = {".xyz", ".top", ".work", ".click", ".biz", ".tk", ".ml", ".ga", ".cf", ".gq", ".info"}
    SHORTENERS = {"bit.ly", "tinyurl.com", "goo.gl", "is.gd", "t.co", "ow.ly", "buff.ly"}
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        return re.findall(url_pattern, text)
    
    @classmethod
    def analyze_url(cls, url: str) -> Dict[str, Any]:
        parsed = urlparse(url if url.startswith("http") else f"http://{url}")
        hostname = parsed.netloc.lower()
        
        score = 0
        reasons = []
        
        # Check for IP Address hostname
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if re.match(ip_pattern, hostname.split(':')[0]):
            score += 35
            reasons.append(f"URL uses a raw IP address ({hostname}) instead of a domain name.")
            
        # Check Suspicious TLDs
        for tld in cls.SUSPICIOUS_TLDS:
            if hostname.endswith(tld):
                score += 25
                reasons.append(f"URL uses a high-risk TLD ({tld}).")
                break
                
        # Check URL Shorteners
        if hostname in cls.SHORTENERS:
            score += 20
            reasons.append(f"URL uses a link shortening service ({hostname}) to mask final destination.")
            
        # Check Excessive Subdomains or Length
        if hostname.count('.') > 3:
            score += 15
            reasons.append("URL contains excessive subdomains, typical of spoofing.")
        if len(url) > 75:
            score += 10
            reasons.append("Abnormally long URL length.")
            
        # Check Targeted Phishing Keywords in URL Path
        phish_words = ["login", "verify", "secure", "update", "banking", "account", "credential", "password"]
        found_keywords = [w for w in phish_words if w in url.lower()]
        if found_keywords:
            score += 15
            reasons.append(f"URL path contains sensitive keywords: {', '.join(found_keywords)}.")
            
        return {
            "url": url,
            "risk_score": min(score, 100),
            "reasons": reasons
        }
    
    @classmethod
    def analyze_all(cls, text: str) -> Dict[str, Any]:
        urls = cls.extract_urls(text)
        results = [cls.analyze_url(u) for u in urls]
        
        max_score = max([r["risk_score"] for r in results], default=0)
        all_reasons = []
        for r in results:
            all_reasons.extend(r["reasons"])
            
        return {
            "url_count": len(urls),
            "urls_analyzed": results,
            "max_url_score": max_score,
            "reasons": list(set(all_reasons))
        }