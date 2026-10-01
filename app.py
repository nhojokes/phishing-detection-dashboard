import streamlit as st
import pandas as pd
import plotly.express as px
from src.parser import EmailParser
from src.url_analyzer import URLAnalyzer
from src.sender_analyzer import SenderAnalyzer
from src.content_analyzer import ContentAnalyzer
from src.ml_engine import MLEngine
from src.risk_engine import RiskEngine
from src.database import Database

# Page Configuration
st.set_page_config(
    page_title="Phishing Detection & Security Awareness Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Initialize System Components
db = Database()
ml = MLEngine()

st.title("🛡️ Phishing Email Detection & SOC Awareness Dashboard")
st.markdown("Automated Email Threat Analysis, Explainable AI Risk Scoring, and Security Training Tool.")

tabs = st.tabs(["📧 Analyze Email", "📊 SOC Analytics Dashboard", "🎓 Phishing Awareness Hub"])

# TAB 1: EMAIL ANALYSIS ENGINE
with tabs[0]:
    st.header("Analyze Email Indicators")
    
    input_method = st.radio("Choose Input Method:", ["Manual Entry", "Upload .eml File"], horizontal=True)
    
    sender_in, subject_in, body_in = "", "", ""
    
    if input_method == "Upload .eml File":
        uploaded_file = st.file_uploader("Upload an .eml email file", type=["eml", "txt"])
        if uploaded_file is not None:
            parsed = EmailParser.parse_eml_file(uploaded_file.read())
            sender_in = parsed["sender"]
            subject_in = parsed["subject"]
            body_in = parsed["body"]
            st.success("File parsed successfully!")
    else:
        sender_in = st.text_input("Sender Email Address:", value="security@paypa1-update.com")
        subject_in = st.text_input("Email Subject:", value="URGENT: Your Account Has Been Locked!")
        body_in = st.text_area("Email Content Body:", value="Dear user, your account was accessed from an unknown device. Please verify your credentials immediately at http://192.168.1.1/login or your account will be deleted.", height=150)

    if st.button("🚀 Analyze Email Threat Level", type="primary"):
        if not body_in.strip():
            st.warning("Please provide email body text to analyze.")
        else:
            # Execute Pipeline
            url_res = URLAnalyzer.analyze_all(body_in)
            sender_res = SenderAnalyzer.analyze(sender_in)
            content_res = ContentAnalyzer.analyze(subject_in, body_in)
            ml_res = ml.predict(f"{subject_in} {body_in}")
            
            risk = RiskEngine.calculate_risk(url_res, sender_res, content_res, ml_res)
            
            # Save Record
            db.insert_record(sender_in, subject_in, risk["final_score"], risk["classification"])
            
            st.divider()
            
            # Results Header
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(label="Overall Risk Score", value=f"{risk['final_score']} / 100")
                if risk["severity"] == "error":
                    st.error(f"Classification: **{risk['classification']}**")
                elif risk["severity"] == "warning":
                    st.warning(f"Classification: **{risk['classification']}**")
                else:
                    st.success(f"Classification: **{risk['classification']}**")
                    
            with col2:
                st.subheader("💡 Why is this marked suspicious? (XAI)")
                for exp in risk["explanations"]:
                    st.write(f"• {exp}")
                    
            st.divider()
            
            # Breakdown Charts
            st.subheader("🔍 Threat Indicator Breakdown")
            df_breakdown = pd.DataFrame(list(risk["breakdown"].items()), columns=["Category", "Score"])
            fig = px.bar(df_breakdown, x="Category", y="Score", color="Score", range_y=[0, 100], color_continuous_scale="Reds")
            st.plotly_chart(fig, use_container_width=True)
            
            # Actionable Security Recommendations
            st.subheader("🛡️ Recommended SOC Actions")
            if risk["final_score"] >= 75:
                st.error("""
                1. **Do NOT click any links or download attachments.**
                2. Report email to internal IT Security / SOC team.
                3. Mark domain in email gateway blocklist.
                4. Reset password if credentials were accidentally submitted.
                """)
            elif risk["final_score"] >= 50:
                st.warning("""
                1. Verify sender identity via an alternative trusted communication channel (Phone, Teams).
                2. Hover over links to inspect the actual destination URL before clicking.
                """)
            else:
                st.info("No immediate malicious indicators detected. Maintain standard security caution.")

# TAB 2: SOC ANALYTICS DASHBOARD
with tabs[1]:
    st.header("SOC Analysis Metrics & History")
    records = db.get_all_records()
    
    if not records:
        st.info("No email analyses recorded yet. Use the first tab to analyze emails!")
    else:
        df_hist = pd.DataFrame(records, columns=["ID", "Timestamp", "Sender", "Subject", "Score", "Classification"])
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Analyzed", len(df_hist))
        c2.metric("High Risk Detected", len(df_hist[df_hist["Classification"] == "HIGH RISK / LIKELY PHISHING"]))
        c3.metric("Average Risk Score", round(df_hist["Score"].mean(), 1))
        
        st.subheader("Classification Distribution")
        fig_pie = px.pie(df_hist, names="Classification", title="Threat Classifications", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.subheader("Historical Log")
        st.dataframe(df_hist, use_container_width=True)

# TAB 3: PHISHING AWARENESS HUB
with tabs[2]:
    st.header("🎓 Security Awareness Training Module")
    st.markdown("""
    ### How to Spot Phishing Indicators:
    
    1. **Lookalike Domains (Typosquatting):**
       - Phishers use domain names similar to real ones (e.g., `paypa1.com` instead of `paypal.com`).
    2. **Urgency and Threats:**
       - "Your account will be closed in 24 hours!" - Phishers create artificial panic to bypass critical thinking.
    3. **Suspicious Destination URLs:**
       - Always inspect the link destination. Watch for raw IP addresses (`http://192.168.1.1`) or cheap TLDs (`.xyz`, `.tk`).
    4. **Mismatched Sender Display Names:**
       - An email displaying "Microsoft Support" but coming from `supplier123@gmail.com`.
    """)
    
    st.divider()
    st.subheader("🧠 Interactive Quick Quiz")
    q1 = st.radio("An email says: 'URGENT: Click here to claim your refund before it expires in 1 hour!' What driver is being used?",
                  ["Reciprocity", "Urgency / Scarcity", "Authority"], index=0)
    if st.button("Submit Answer"):
        if q1 == "Urgency / Scarcity":
            st.success("Correct! Attackers use artificial urgency to push targets into rapid mistakes.")
        else:
            st.error("Incorrect. Try again! Look for time-pressure cues.")