import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def generate_synthetic_data(filepath: str):
    data = [
        # Phishing Examples
        {"text": "URGENT: Your bank account has been locked! Click http://login-secure-update-bank.com immediately to restore access.", "label": 1},
        {"text": "Action Required: Verify your PayPal account credentials within 24 hours at http://192.168.1.1/login or your account will be suspended.", "label": 1},
        {"text": "Dear customer, you have won $10,000! Click here http://bit.ly/claim-prize-now to claim your reward.", "label": 1},
        {"text": "Security Alert: Microsoft Office 365 password expiring today. Update now at http://microsoft-auth-service-portal.xyz.", "label": 1},
        {"text": "Invoice Overdue: Please download the attachment and complete payment immediately at http://overdue-invoice-portal.top.", "label": 1},
        {"text": "Your Amazon order has been suspended. Update your credit card at http://amazon-account-verify.info.", "label": 1},
        {"text": "IT Helpdesk: Critical password reset required for all employees. Go to http://company-it-desk.tk.", "label": 1},
        {"text": "Important Tax Document Available. Access your W2 form now at http://irs-tax-portal-online.biz.", "label": 1},
        
        # Legitimate Examples
        {"text": "Hi Team, please find attached the meeting notes from yesterday's project sync. Best regards, Sarah.", "label": 0},
        {"text": "Your monthly statement for account ending in 4321 is now available in your official online banking app.", "label": 0},
        {"text": "Reminder: Annual company townhall scheduled for Thursday at 10 AM EST in Conference Room B.", "label": 0},
        {"text": "Thanks for your order! Your tracking number is 1Z9999999999999999. Track package on official UPS portal.", "label": 0},
        {"text": "Security Alert: New login detected from Chrome on MacOS. If this was you, no action is needed.", "label": 0},
        {"text": "Your weekly performance analytics report is ready for download in the HR internal dashboard.", "label": 0},
        {"text": "Hey, are we still meeting for lunch today at 12:30 PM?", "label": 0},
        {"text": "Project update: Sprint retrospective results have been updated in Jira.", "label": 0}
    ]
    
    # Expand dataset artificially for robust demo training
    data = data * 20
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"[+] Synthetic dataset written to {filepath}")
    return df

def train_and_save_model():
    os.makedirs("models", exist_ok=True)
    data_path = os.path.join("data", "synthetic_phishing_dataset.csv")
    df = generate_synthetic_data(data_path)
    
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_vec, y_train)
    
    preds = clf.predict(X_test_vec)
    print("\n[+] Model Training Complete. Evaluation Report:")
    print(classification_report(y_test, preds))
    
    joblib.dump(clf, "models/model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    print("[+] Model & Vectorizer saved in models/")

if __name__ == "__main__":
    train_and_save_model()