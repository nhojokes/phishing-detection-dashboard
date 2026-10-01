from src.sender_analyzer import SenderAnalyzer

def test_brand_impersonation():
    res = SenderAnalyzer.analyze("PayPal Security <support@paypal-security-update.com>")
    assert res["risk_score"] > 0
    # Search for 'brand' in the reason output
    assert any("brand" in r.lower() for r in res["reasons"])