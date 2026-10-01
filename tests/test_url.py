from src.url_analyzer import URLAnalyzer

def test_ip_url_detection():
    res = URLAnalyzer.analyze_url("http://192.168.1.1/login")
    assert res["risk_score"] >= 35
    assert any("raw IP address" in r for r in res["reasons"])

def test_suspicious_tld():
    res = URLAnalyzer.analyze_url("http://secure-update.xyz")
    assert res["risk_score"] >= 25
    assert any("high-risk TLD" in r for r in res["reasons"])