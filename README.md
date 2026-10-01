# 🛡️ Phishing Email Detection & SOC Awareness Dashboard

An industry-focused defensive cybersecurity application that combines rule-based heuristics, dynamic header parsing, URL threat extraction, and machine learning to analyze phishing risks in real time.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/gui-streamlit-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Key Features

- **Multi-Layer Analysis Engine:** Combines heuristics, indicator analysis, and supervised machine learning (Random Forest + TF-IDF).
- **Explainable AI (XAI) Output:** Provides security analysts and users with granular explanations for flagged risks.
- **Header & File Parsing:** Parses raw text or standard `.eml` email files seamlessly.
- **SOC Incident Logging:** Local SQLite database stores analysis logs for audit trails and security analytics.
- **Security Awareness Hub:** Built-in educational material and interactive quizzes for user awareness training.

---

## Threat Detection Methodology

| Module | Inspection Target | Risk Factors |
| :--- | :--- | :--- |
| **URL Analyzer** | Extracted Links | IP hostnames, high-risk TLDs (`.xyz`, `.top`), link shorteners, sensitive paths |
| **Sender Engine** | `From` Headers | Typosquatting, brand impersonation, display name mismatches |
| **Content Engine** | Subject & Body | Urgency pressure, financial lures, fear tactics |
| **ML Predictor** | Entire Message Text | Text vectorization with TF-IDF and Random Forest classification |

---

## Quickstart

```bash
git clone [https://github.com/your-username/phishing-email-detection-dashboard.git](https://github.com/your-username/phishing-email-detection-dashboard.git)
cd phishing-email-detection-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train.py
streamlit run app.py