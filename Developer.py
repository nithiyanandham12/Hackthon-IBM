import streamlit as st
import random
import time
import requests
import plotly.graph_objs as go

# Dummy history of developer tasks
@st.cache_data
def get_developer_history():
    return [
        {"date": "2025-04-18", "task": "Wrote custom parsing logic for logs manually"},
        {"date": "2025-04-19", "task": "Manually tested edge cases for REST API"},
        {"date": "2025-04-20", "task": "Refactored legacy code without tools"},
    ]

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
    time.sleep(2)
    return "✔️ Questions generated using IBM Granite AI Engine!"

def show_skill_productivity_meters(monotony_before=78, productivity_before=70, skill_before=60,
                                    monotony_after=None, productivity_after=None, skill_after=None):
    st.markdown("## 📈 Developer Engagement Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Monotony Score", f"{monotony_before}%" if not monotony_after else f"{monotony_after}%",
                  delta=f"{monotony_after - monotony_before}%" if monotony_after else None)
    with col2:
        st.metric("⚙️ Productivity", f"{productivity_before}%" if not productivity_after else f"{productivity_after}%",
                  delta=f"+{productivity_after - productivity_before}%" if productivity_after else None)
    with col3:
        st.metric("💡 Skill Growth", f"{skill_before}%" if not skill_after else f"{skill_after}%",
                  delta=f"+{skill_after - skill_before}%" if skill_after else None)

    st.markdown("### 📊 Developer Skill Wheel")
    labels = ['Debugging', 'Prompting', 'Scripting', 'Automation']
    values_before = [60, 30, 50, 40]
    values_after = [v + (skill_after - skill_before if skill_after else 0) for v in values_before]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values_after if skill_after else values_before, hole=.4)])
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig, use_container_width=True)

# Prompt Engineering MCQs for Python Developers
def get_python_mcq_challenges():
    return [
        {"question": "What is prompt engineering primarily used for in AI development?",
         "options": ["A. Tuning database queries", "B. Designing ML models", "C. Structuring input to get desired AI output", "D. Frontend design"],
         "answer": "C. Structuring input to get desired AI output"},

        {"question": "Which of the following prompts will best generate Python code for an API?",
         "options": ["A. Write code", "B. Create something", "C. Generate a FastAPI endpoint for user login with JWT", "D. Help me"],
         "answer": "C. Generate a FastAPI endpoint for user login with JWT"},

        {"question": "Why is 'chain-of-thought' prompting useful in coding?",
         "options": ["A. It makes the AI guess randomly", "B. It breaks the request into logical steps for better results", "C. It formats the code", "D. It optimizes memory"],
         "answer": "B. It breaks the request into logical steps for better results"},

        {"question": "How can you use prompt engineering to automate unit test generation?",
         "options": ["A. Tell the model to ‘write tests’", "B. Feed the function and say: ‘Generate pytest tests with mocks for this function’", "C. Ask it to debug", "D. Use @pytest decorator"],
         "answer": "B. Feed the function and say: ‘Generate pytest tests with mocks for this function’"},

        {"question": "Which of these improves prompt clarity the most?",
         "options": ["A. Vague instructions", "B. Technical terms only", "C. Examples and constraints", "D. Asking ‘please’"],
         "answer": "C. Examples and constraints"},

        {"question": "Prompt engineering is most useful in which phase?",
         "options": ["A. Code compilation", "B. Project deployment", "C. Code generation, data analysis, and documentation", "D. Network setup"],
         "answer": "C. Code generation, data analysis, and documentation"},

        {"question": "What prompt would best extract key functions from a Python file?",
         "options": ["A. Summarize file", "B. Analyze", "C. List key functions with docstrings and explain their purpose", "D. Explain"],
         "answer": "C. List key functions with docstrings and explain their purpose"}
    ]

# UI Flow
if not st.session_state.get("quiz_started", False):
    st.title("👨‍💻 DevSprint Challenge Arena")
    st.markdown("""
    Welcome, Developer! 🧑‍💻 You're halfway through debugging legacy Python scripts.
    
    🧠 What if you didn’t have to do *everything* manually?
    
    This arena introduces you to **Prompt Engineering** — your new secret weapon ⚡  
    Let's see how much time and effort it can save you using tools like **IBM Granite AI**.
    """)
    st.video("https://youtu.be/IbVjxg9bHAw?si=rTi5O2OB5tDI8ecf")  # Replace with your explainer video

    if 'video_confirmed' not in st.session_state:
        st.session_state.video_confirmed = False
    st.session_state.video_confirmed = st.checkbox("✅ I've watched the video and I'm ready for the quiz")

    if not st.session_state.video_confirmed:
        st.warning("👀 Please complete the video before proceeding.")
        st.stop()

    if st.button("🚀 Generate My AI Developer Quiz"):
        with st.spinner("⏳ Fetching recent dev activities..."):
            time.sleep(1)
        with st.spinner("🧠 Creating challenge using IBM Granite..."):
            generate_questions_with_granite()
        st.session_state.quiz_started = True
        st.rerun()

else:
    st.markdown("### 🔄 Initializing Developer Challenge...")
    progress = st.empty()
    status = st.empty()

    steps = [
        "📂 Reviewing your manual development tasks...",
        "🤖 Initializing prompt-based alternatives...",
        "📦 Packaging your personalized challenge..."
    ]

    for i, step in enumerate(steps):
        progress.progress((i + 1) / len(steps), text=step)
        status.markdown(step)
        time.sleep(1.5)

    progress.empty()
    status.empty()

    st.subheader("Before Challenge")
    show_skill_productivity_meters()

    challenges = get_python_mcq_challenges()
    user_answers = {}

    with st.form("python_prompt_form"):
        for i, challenge in enumerate(challenges):
            st.markdown(f"### {i+1}. {challenge['question']}")
            user_answers[i] = st.radio("Choose one:", challenge['options'], key=f"q{i}")
            st.markdown("---")
        submitted = st.form_submit_button("✅ Submit My Answers")

    if submitted:
        score = sum(1 for i, challenge in enumerate(challenges) if user_answers[i] == challenge['answer'])
        st.success(f"🎉 You scored {score} out of {len(challenges)}!")

        if score >= 5:
            st.success("🏅 You’ve earned the **Prompt Engineering Beginner Badge**!")
            st.balloons()

        st.subheader("After Challenge")
        show_skill_productivity_meters(
            monotony_after=65, productivity_after=85, skill_after=80
        )

        st.markdown("### ⚡ Ready to use this in your projects?")
        real_use = st.radio(
            "Would you apply prompt engineering for Python tasks now?",
            ["Yes", "Maybe later", "No"],
            key="apply_skill_feedback"
        )

        if real_use == "Yes":
            st.success("🚀 Let’s go! You’re on your way to faster development with AI.")
        elif real_use == "Maybe later":
            st.info("⏳ Got it. We'll remind you when you're ready.")
        elif real_use == "No":
            st.info("📌 No problem. You can always revisit this challenge.")
