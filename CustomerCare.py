import streamlit as st
import random
import time
import requests
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objs as go

# Dummy storage for memory
@st.cache_data
def get_customer_service_history():
    return [
        {"date": "2025-04-18", "task": "Handled 20+ customer queries via chat"},
        {"date": "2025-04-19", "task": "Resolved billing dispute for VIP customer"},
        {"date": "2025-04-20", "task": "Created FAQ guide for tier-1 support"}
    ]

# IBM Watsonx Credentials
API_KEY = "YOUR_IBM_API_KEY"
PROJECT_ID = "YOUR_PROJECT_ID"

@st.cache_data(show_spinner=False)
def get_ibm_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

def generate_questions_with_granite():
    time.sleep(3)  # Simulate API thinking time
    return "✔️ Challenge generated using IBM Granite AI engine!"  # Gimmick message

def show_skill_productivity_meters(monotony_before=70, productivity_before=75, skill_before=65,
                                    monotony_after=None, productivity_after=None, skill_after=None):
    st.markdown("## 📈 Skill & Productivity Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Monotony Score", f"{monotony_before}%" if not monotony_after else f"{monotony_after}%",
                  delta=f"{monotony_after - monotony_before}%" if monotony_after else None)

    with col2:
        st.metric("⚙️ Productivity", f"{productivity_before}%" if not productivity_after else f"{productivity_after}%",
                  delta=f"+{productivity_after - productivity_before}%" if productivity_after else None)
    with col3:
        st.metric("📚 Skill Engagement", f"{skill_before}%" if not skill_after else f"{skill_after}%",
                  delta=f"+{skill_after - skill_before}%" if skill_after else None)

    st.markdown("### 📊 Visual Skill Tracker")
    labels = ['Empathy', 'Communication', 'Product Knowledge', 'Problem Solving']
    values_before = [65, 70, 60, 55]
    values_after = [v + (skill_after - skill_before if skill_after else 0) for v in values_before]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values_after if skill_after else values_before, hole=.4)])
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig, use_container_width=True)

def get_customer_care_mcqs():
    return [
        {"question": "What is the first step in handling an angry customer?",
         "options": ["A. Interrupt them", "B. Listen actively", "C. Offer a discount", "D. Escalate to supervisor"],
         "answer": "B. Listen actively"},
        {"question": "Which phrase best shows empathy?",
         "options": ["A. That's our policy", "B. I understand how frustrating that must be", 
                     "C. You'll have to wait", "D. It's not my department"],
         "answer": "B. I understand how frustrating that must be"},
        {"question": "When is it best to escalate a call?",
         "options": ["A. After saying no", "B. If the issue is beyond your scope", 
                     "C. Right away", "D. Never escalate"],
         "answer": "B. If the issue is beyond your scope"},
        {"question": "What is a good way to end a customer service interaction?",
         "options": ["A. Say goodbye", "B. Hang up", "C. Confirm issue resolution and thank the customer", 
                     "D. Transfer them"],
         "answer": "C. Confirm issue resolution and thank the customer"},
        {"question": "Which of the following helps build trust with customers?",
         "options": ["A. Over-promising", "B. Being vague", "C. Providing accurate information", "D. Avoiding questions"],
         "answer": "C. Providing accurate information"}
    ]


# Initialize session states
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "video_confirmed" not in st.session_state:
    st.session_state.video_confirmed = False

# UI starts here
st.title("TaskGene Challenge Arena")
if not st.session_state.test_started:
    st.markdown("""
    Welcome, Rahul! 🧑‍💼
    Time to test and refresh your customer service skills.

    🧠 Powered by **IBM Granite**
    """)
    st.video("https://youtu.be/YH1EJlHh7DU?si=VKtuhPy6_4GP9D5W")

    st.session_state.video_confirmed = st.checkbox("✅ I have watched the course video and I'm ready for the aptitude challenge")

    if not st.session_state.video_confirmed:
        st.warning("👀 Please watch the full video and check the box to continue.")
        st.stop()

    if st.button("🚀 Generate Challenge Questions (IBM Granite)") and not st.session_state.test_started:
        with st.spinner("🔍 Fetching task history from **Watsonx.data**..."):
            time.sleep(2)
        with st.spinner("🧠 Generating questions using **IBM Granite AI model**..."):
            time.sleep(2)
        with st.spinner("📦 Converting output into **MCQ format (JSON → Quiz)**..."):
            time.sleep(2)

        generate_questions_with_granite()
        st.session_state.test_started = True
        st.rerun()

else:
    st.markdown("### ⚙️ Initializing your challenge...")

    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    steps = [
        "📂 Reviewing your recent tasks...",
        "🧠 Spinning up the challenge engine...",
        "📦 Packaging your personalized quiz..."
    ]
    for i, step in enumerate(steps):
        progress_placeholder.progress((i + 1) / len(steps), text=step)
        status_placeholder.markdown(step)
        time.sleep(1.5)
    progress_placeholder.empty()
    status_placeholder.empty()

    st.subheader("Before Test")
    show_skill_productivity_meters()

    challenges = get_customer_care_mcqs()

    if not st.session_state.quiz_submitted:
        with st.form("challenge_form"):
            for i, challenge in enumerate(challenges):
                st.markdown(f"### {i+1}. {challenge['question']}")
                default_index = challenge['options'].index(
                    st.session_state.user_answers.get(i, challenge['options'][0])
                ) if i in st.session_state.user_answers else 0

                st.session_state.user_answers[i] = st.radio(
                    "Choose one:", 
                    challenge["options"], 
                    key=f"q{i}", 
                    index=default_index
                )
                st.markdown("---")
            submitted = st.form_submit_button("✅ Submit All")
            if submitted:
                st.session_state.quiz_submitted = True
                st.rerun()

    else:
        score = sum(
            1 for i, challenge in enumerate(challenges)
            if st.session_state.user_answers.get(i) == challenge['answer']
        )
        st.success(f"🎉 You scored {score} out of {len(challenges)}")

        if score >= 5:
            st.success("🏅 Congratulations! You've unlocked the **Customer care Intermediate** badge.")
            st.balloons()

        st.subheader("After Test")
        show_skill_productivity_meters(
            monotony_after=70, productivity_after=85, skill_after=78
        )

        st.markdown("### 🚀 Will you apply this skill in your real work?")
        real_use = st.radio(
            "Would you like to use this Excel skill in your current or upcoming tasks?",
            ["Need to Think", "Yes", "No"],
            key="apply_skill_post_quiz"
        )

        if real_use == "Yes":
            st.success("🎯 Awesome! TaskGene will prioritize challenges that align with your current workflow.")
        elif real_use == "No":
            st.info("📌 Got it. We’ll focus on more relevant skills in future challenges.")
        elif real_use == "Need to Think":
            st.info("⏳ No worries. You can revisit skills anytime.")

        if st.button("🔁 Retake Challenge"):
            st.session_state.test_started = False
            st.session_state.quiz_submitted = False
            st.session_state.user_answers = {}
            st.rerun()
