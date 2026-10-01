from src.content_analyzer import ContentAnalyzer

def test_urgency_keyword_detection():
    res = ContentAnalyzer.analyze("URGENT NOTICE", "Your account will be suspended within 24 hours.")
    assert res["urgency_count"] >= 2
    assert res["risk_score"] > 0