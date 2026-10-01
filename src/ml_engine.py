import os
import joblib
from typing import Dict, Any

class MLEngine:
    """Supervised Machine Learning Phishing Probability Predictor."""
    
    def __init__(self, model_dir: str = "models"):
        self.model_path = os.path.join(model_dir, "model.pkl")
        self.vec_path = os.path.join(model_dir, "vectorizer.pkl")
        self.model = None
        self.vectorizer = None
        self.is_loaded = self._load()

    def _load(self) -> bool:
        if os.path.exists(self.model_path) and os.path.exists(self.vec_path):
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vec_path)
            return True
        return False

    def predict(self, text: str) -> Dict[str, Any]:
        if not self.is_loaded:
            return {
                "phishing_probability": 0.0,
                "ml_score": 0,
                "status": "Model not trained. Run train.py first."
            }
            
        vec_text = self.vectorizer.transform([text])
        prob = float(self.model.predict_proba(vec_text)[0][1])
        
        return {
            "phishing_probability": round(prob, 4),
            "ml_score": int(prob * 100),
            "status": "Success"
        }