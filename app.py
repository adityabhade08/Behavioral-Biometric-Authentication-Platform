import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import time

st.set_page_config(page_title="Behavioral Biometric Auth", layout="wide")

# -------------------------------
# SESSION STATE
# -------------------------------
if "model" not in st.session_state:
    st.session_state.model = None

if "trust_score" not in st.session_state:
    st.session_state.trust_score = 100

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# UTILITY FUNCTIONS
# -------------------------------
def generate_behavior(normal=True):
    """
    Simulates user behavior.
    Normal = genuine user
    Abnormal = attacker / bot
    """
    if normal:
        return [
            np.random.normal(120, 10),   # typing speed
            np.random.normal(0.25, 0.03),# key hold time
            np.random.normal(400, 50),   # mouse speed
            np.random.normal(0.6, 0.05)  # scroll pause ratio
        ]
    else:
        return [
            np.random.normal(200, 30),
            np.random.normal(0.05, 0.01),
            np.random.normal(900, 120),
            np.random.normal(0.1, 0.02)
        ]

def calculate_trust(score):
    return int((score + 0.5) * 100)

# -------------------------------
# UI
# -------------------------------
st.title("🔐 Behavioral Biometric Continuous Authentication")
st.caption("AI-driven passwordless & continuous authentication system")

st.divider()

# -------------------------------
# ENROLLMENT
# -------------------------------
st.subheader("1️⃣ User Enrollment (Baseline Creation)")

if st.button("Enroll User"):
    baseline = np.array([generate_behavior(True) for _ in range(100)])
    model = IsolationForest(contamination=0.05)
    model.fit(baseline)

    st.session_state.model = model
    st.session_state.logged_in = True
    st.success("✅ Behavioral baseline created successfully")

# -------------------------------
# CONTINUOUS AUTHENTICATION
# -------------------------------
st.subheader("2️⃣ Continuous Authentication Monitoring")

if st.session_state.logged_in and st.session_state.model is not None:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Live Trust Score")
        trust_placeholder = st.empty()

    with col2:
        st.markdown("### 🚨 Security Status")
        alert_placeholder = st.empty()

    attack = st.toggle("⚠️ Simulate Attacker Behavior")

    for _ in range(10):
        behavior = np.array(generate_behavior(not attack)).reshape(1, -1)
        score = st.session_state.model.decision_function(behavior)[0]
        trust = calculate_trust(score)

        st.session_state.trust_score = trust

        trust_placeholder.metric(
            label="Trust Score",
            value=f"{trust} / 100",
            delta=None
        )

        if trust < 40:
            alert_placeholder.error("🚫 Session Terminated: High Risk Detected")
            st.session_state.logged_in = False
            break
        elif trust < 60:
            alert_placeholder.warning("⚠️ Step-Up Authentication Required")
        else:
            alert_placeholder.success("🟢 Session Secure")

        time.sleep(1)

else:
    st.info("👆 Please enroll user to start monitoring")

# -------------------------------
# RISK DASHBOARD
# -------------------------------
st.divider()
st.subheader("3️⃣ Risk Assessment Summary")

risk_data = pd.DataFrame({
    "Risk": [
        "Credential Theft",
        "Session Hijacking",
        "Insider Threat",
        "Bot Attack"
    ],
    "Likelihood": ["High", "Medium", "Medium", "High"],
    "Impact": ["High", "High", "High", "Medium"],
    "Mitigation": [
        "Behavioral Biometrics",
        "Continuous Authentication",
        "Behavior Deviation Detection",
        "Anomaly Detection"
    ]
})

st.dataframe(risk_data, use_container_width=True)

st.caption("Mapped to ISO 27001, NIST Zero Trust & SOC 2")
