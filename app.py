# app.py

# --- Imports ---
from langgraph.graph import StateGraph
from typing import TypedDict, List
import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import time

# --- Streamlit Config ---
st.set_page_config(page_title="LangGraph Agentic Workflow", page_icon="🤖", layout="centered")

# --- Theme Toggle ---
st.sidebar.title("🎨 UI Settings")
theme = st.sidebar.radio("Choose Theme", ("🌞 Light", "🌙 Dark"))
if theme == "🌙 Dark":
    bg_color = "#1e1e1e"
    text_color = "#ffffff"
    card_color = "#333333"
else:
    bg_color = "#f8f9fa"
    text_color = "#000000"
    card_color = "#ffffff"

# --- Load Environment & Groq Client ---
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Agent State Definition ---
class AgentState(TypedDict):
    query: str
    sub_tasks: List[str]
    current_task: str
    results: List[str]
    feedback: str
    iterations: int

# --- Utility: Ask Groq ---
def ask_groq(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# --- Agent Definitions ---
def plan_agent(state: AgentState) -> AgentState:
    prompt = f"Split the following query into 3 concise sub-tasks:\n{state['query']}"
    sub_tasks = ask_groq(prompt).split('\n')
    state["sub_tasks"] = [task.strip("1234567890.- ").strip() for task in sub_tasks if task.strip()]
    return state

def tool_agent(state: AgentState) -> AgentState:
    if not state.get("results"):
        state["results"] = []
    if not state["sub_tasks"]:
        return state
    task = state["sub_tasks"].pop(0)
    result = ask_groq(f"Do this task:\n{task}")
    state["results"].append(result)
    state["current_task"] = task
    return state

def reflection_agent(state: AgentState) -> AgentState:
    results = "\n".join(state["results"])
    feedback = ask_groq(f"Review the following results and give feedback on whether they solve the original query well:\n\n{results}")
    state["feedback"] = feedback.strip()
    state["iterations"] += 1
    return state

def decide_next(state: AgentState) -> str:
    return "__end__" if state["iterations"] >= 3 else "PlanAgent"

# --- LangGraph Definition ---
graph = StateGraph(AgentState)
graph.add_node("PlanAgent", plan_agent)
graph.add_node("ToolAgent", tool_agent)
graph.add_node("ReflectionAgent", reflection_agent)
graph.set_entry_point("PlanAgent")
graph.add_edge("PlanAgent", "ToolAgent")
graph.add_edge("ToolAgent", "ReflectionAgent")
graph.add_conditional_edges("ReflectionAgent", decide_next)
compiled_graph = graph.compile()

# --- Streamlit UI ---

# --- Header Banner ---
st.markdown(
    f"""
    <div style="text-align:center; padding: 1.5rem 1rem; background: linear-gradient(to right, #8e44ad, #3498db); border-radius: 10px;">
        <h1 style="color:white;">🤖 Agentic Workflow Playground</h1>
        <h4 style="color:white;">LangGraph + Groq + Streamlit</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Step Tracker ---
st.markdown("### 📍 Progress Tracker")
st.markdown("✅ **PlanAgent** 🔧 **ToolAgent** 🪞 **ReflectionAgent**")

# --- Query Input ---
st.markdown("## 💬 What's your query?")
user_query = st.text_area(
    "Let the agents solve your task with reasoning steps.",
    placeholder="e.g., Summarize customer complaints and identify top 3 issues.",
    height=100
)
run_button = st.button("🚀 Run Agentic Workflow")

# --- Agent Avatars ---
agent_icons = {
    "PlanAgent": "🧠",
    "ToolAgent": "🛠️",
    "ReflectionAgent": "🪞"
}

# --- Workflow Execution ---
if run_button:
    if not user_query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("⚙️ Agents are collaborating..."):
            time.sleep(1.2)
            initial_state: AgentState = {
                "query": user_query,
                "sub_tasks": [],
                "current_task": "",
                "results": [],
                "feedback": "",
                "iterations": 0
            }
            final_state = compiled_graph.invoke(initial_state)

        # --- Result Display ---
        st.markdown("## 📋 Sub-Task Results")
        for idx, res in enumerate(final_state["results"], 1):
            st.info(f"{agent_icons['ToolAgent']} **Task {idx}:** {res}")

        # --- Feedback ---
        st.markdown("## 🪞 Final Reflection")
        st.success(f"{agent_icons['ReflectionAgent']} {final_state['feedback']}")

        # --- Debug Info ---
        with st.expander("🧪 Debug Info"):
            st.json({
                "Initial State": initial_state,
                "Final State": final_state
            })

# --- Footer ---
st.markdown("---")
st.markdown(
    f"<div style='text-align:center; color:{text_color};'>Built with ❤️ <b>LangGraph</b>, <b>Groq</b>, and <b>Streamlit</b></div>",
    unsafe_allow_html=True
)
