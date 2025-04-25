from dotenv import load_dotenv
import os
import requests
import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np
import random

# Load secrets from .env
load_dotenv()
IBM_API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

# Get IBM Access Token
def get_ibm_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# Send request to IBM Granite model on Watsonx
def send_chunk_to_watsonx(chunk_text, access_token, prompt_prefix):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-01-15"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "input": prompt_prefix + chunk_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 8000,
            "min_new_tokens": 0,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        "model_id": "mistralai/mistral-large",
        "project_id": PROJECT_ID
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        result = response.json()
        return result["results"][0]["generated_text"]
    except Exception as e:
        return f"⚠️ Watsonx error: {str(e)}\n\nResponse: {response.text}"

# Page config and navigation
st.set_page_config(layout="wide")
st.sidebar.title("👔 Raj's Manager Panel")
st.sidebar.markdown("Keep your team thriving with IBM Granite AI insights.")
nav = st.sidebar.radio("📂 Navigate", [
    "Engagement Overview", "Team Insights", "Skill Heatmap", 
    "Workload Distribution", "Engagement Trends", "Suggestions", "HR Report", "Pinned Tasks"
])

# Dummy Data
token = get_ibm_access_token(IBM_API_KEY)
team_members = [
    "Priya", "Arjun Mehta", "Sneha Iyer", "Rahul Verma",
    "Aisha Khan", "Karan Patel", "Neha Reddy", "Vikram Das",
    "Divya Nair", "Rohit Sen", "Meera Joseph", "Ankit Rao"
]
monotony_scores = [random.randint(35, 85) for _ in team_members]
productivity_scores = [random.randint(65, 100) for _ in team_members]
skill_matrix = pd.DataFrame(np.random.randint(0, 10, size=(12, 4)),
                            columns=["Excel", "Python", "Viz", "Reporting"],
                            index=team_members)
weekly_trends = pd.DataFrame({
    "Week": pd.date_range(end=pd.Timestamp.today(), periods=6, freq="W"),
    "Avg Monotony": [random.randint(45, 75) for _ in range(6)],
    "Avg Productivity": [random.randint(60, 95) for _ in range(6)]
})

# Engagement Overview
if nav == "Engagement Overview":
    st.title("📊 Team Engagement Overview (Powered by IBM Granite)")

    st.subheader("🔥 Monotony Hotspots")
    mono_df = pd.DataFrame({
        "Team Member": team_members,
        "Monotony Score (%)": monotony_scores
    })
    fig = px.bar(mono_df.sort_values(by="Monotony Score (%)", ascending=False),
                 x='Monotony Score (%)', y='Team Member', orientation='h',
                 color='Monotony Score (%)', color_continuous_scale='reds')
    st.plotly_chart(fig, use_container_width=True)

    ai_insight = send_chunk_to_watsonx(mono_df.to_csv(index=False), token, "From these monotony scores, identify the highest, lowest, and average values. Mention any outliers or potential burnout risks using IBM Granite insights.:\n")
    st.info(f"🧠 IBM Granite Insight: {ai_insight}")

    st.subheader("⚙️ Productivity Overview")
    prod_df = pd.DataFrame({
        "Team Member": team_members,
        "Productivity (%)": productivity_scores
    })
    fig2 = px.bar(prod_df.sort_values(by="Productivity (%)"),
                  x='Productivity (%)', y='Team Member', orientation='h',
                  color='Productivity (%)', color_continuous_scale='greens')
    st.plotly_chart(fig2, use_container_width=True)

    ai_prod = send_chunk_to_watsonx(prod_df.to_csv(index=False), token, "Review these productivity scores. Highlight the highest and lowest performers, calculate the average, and offer a quick insight into team efficiency using IBM Granite.:\n")
    st.info(f"🧠 IBM Granite Insight: {ai_prod}")

# Team Insights
elif nav == "Team Insights":
    st.title("🧑‍💼 Team Member Deep Dive (IBM Granite)")
    selected = st.selectbox("Select Team Member", team_members)
    st.metric("😐 Monotony", f"{monotony_scores[team_members.index(selected)]}%")
    st.metric("⚙️ Productivity", f"{productivity_scores[team_members.index(selected)]}%")
    st.dataframe(skill_matrix.loc[[selected]])
    insight = send_chunk_to_watsonx(f"Monotony: {monotony_scores[team_members.index(selected)]}, Productivity: {productivity_scores[team_members.index(selected)]}, Skills: {skill_matrix.loc[selected].to_dict()}", token, f"Given this team member’s monotony, productivity, and skill data, summarize engagement status and suggest a short development path using IBM Granite AI.:\n")
    st.info(f"🧠 IBM Granite Insight: {insight}")

# Skill Heatmap
elif nav == "Skill Heatmap":
    st.title("🌐 Skill Heatmap Across Team (IBM Granite)")
    st.markdown("Visualize micro-challenge growth areas")
    fig = px.imshow(skill_matrix, 
                    labels=dict(x="Skill", y="Team Member", color="Credential Count"),
                    aspect="auto", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)
    insight = send_chunk_to_watsonx(skill_matrix.to_csv(), token, "Analyze this skill matrix. Identify top-skilled areas and least-developed skills across the team. Suggest training focus based on IBM Granite insights.:\n")
    st.info(f"🧠 IBM Granite Insight: {insight}")

# Workload Distribution
elif nav == "Workload Distribution":
    st.title("📊 Team Workload Overview (IBM Granite)")
    task_distribution = {
        "Reporting": random.randint(10, 25),
        "Excel Analysis": random.randint(10, 20),
        "Email Management": random.randint(5, 15),
        "Client Calls": random.randint(5, 10),
        "Ad Hoc Tasks": random.randint(5, 10)
    }
    fig = px.pie(values=list(task_distribution.values()), 
                 names=list(task_distribution.keys()), 
                 title="Workload Distribution (This Week)",
                 hole=0.3)
    st.plotly_chart(fig)
    workload_text = ", ".join([f"{k}: {v}" for k, v in task_distribution.items()])
    insight = send_chunk_to_watsonx(workload_text, token, "From this workload breakdown, list the most and least time-consuming tasks. Evaluate if the load is balanced and provide a short IBM Granite suggestion.:\n")
    st.info(f"🧠 IBM Granite Insight: {insight}")

# Engagement Trends
elif nav == "Engagement Trends":
    st.title("📈 Engagement Trends Over Time (IBM Granite)")
    fig = px.line(weekly_trends, x="Week", y=["Avg Monotony", "Avg Productivity"],
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📉 Correlation: Monotony vs Productivity")
    df_corr = pd.DataFrame({
        "Monotony": monotony_scores,
        "Productivity": productivity_scores
    })
    fig_corr = px.scatter(df_corr, x="Monotony", y="Productivity",
                          trendline="ols", color=team_members)
    st.plotly_chart(fig_corr)
    insight = send_chunk_to_watsonx(weekly_trends.to_csv(index=False), token, "Analyze these weekly trends for average monotony and productivity. Point out peak and dip weeks. Provide insights into how engagement changed using IBM Granite.:\n")
    st.info(f"🧠 IBM Granite Insight: {insight}")

# Suggestions
elif nav == "Suggestions":
    st.title("💡 AI-Powered Suggestions (IBM Granite)")
    st.warning("🔄 4 members may benefit from creative project swaps:")
    st.markdown("""
    - Team Member 3 🔁 Team Member 8  
    - Team Member 6 🔁 Team Member 11  
    - Team Member 2 🔁 Team Member 9  
    """)
    st.info("✨ Creative switches can reduce burnout and spark innovation.")
    suggestion_text = "Suggest reasons these swaps might work based on engagement and skill diversity."
    ai_suggestions = send_chunk_to_watsonx(suggestion_text, token, "Based on engagement and skill data, explain why the proposed team swaps are beneficial. Keep it factual and supported by IBM Granite AI logic.:\n")
    st.info(f"🧠 IBM Granite Insight: {ai_suggestions}")
    st.button("📤 Notify Team")

# HR Report
elif nav == "HR Report":
    st.title("🏆 Quarterly HR Highlights (Powered by IBM Granite)")
    st.success("🎉 0% team turnover vs 24% department average")
    st.markdown("""
    - 🎓 42 upskilling events
    - ✅ 3 promotions
    - 💬 98% peer feedback participation
    """)
    report_text = "HR Report: 42 upskilling, 3 promotions, 98% feedback, 0% attrition."
    ai_hr = send_chunk_to_watsonx(report_text, token, "Summarize key HR metrics: highlight achievements and average participation rates. Mention any exceptional performance using IBM Granite insights.:\n")
    st.info(f"🧠 IBM Granite Insight: {ai_hr}")
    st.download_button("📄 Download HR Summary", data="HR Report Summary", file_name="hr_summary.pdf")

# Pinned Tasks
elif nav == "Pinned Tasks":
    st.title("📌 Manager's Action Board (IBM Granite)")
    st.markdown("""
    - ✅ Review monotony scores >70%
    - 🔄 Send swap suggestions to HR
    - 🎯 Create 1 new creative challenge
    - 📅 Set 1:1s with Team Member 6 and 11
    """)
    st.checkbox("Mark as done")
    st.text_area("📝 Add New Task")
    tasks_text = "Review monotony, swaps, challenges, 1:1s"
    task_ai = send_chunk_to_watsonx(tasks_text, token, "From these tasks, identify priority based on impact and urgency. Suggest which should be done first, and why, using IBM Granite analysis.:\n")
    st.info(f"🧠 IBM Granite Insight: {task_ai}")
