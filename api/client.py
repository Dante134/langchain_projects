import requests
import streamlit as st

# Config
BASE_URL = "http://localhost:8000"

# Helper function (safe API call)
def call_api(endpoint, payload):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        response.raise_for_status()
        data = response.json()

        # Handle both response types
        output = data.get("output")

        if isinstance(output, dict):  # OpenAI response
            return output.get("content", "No content found")
        else:  # Ollama response (string)
            return output

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Streamlit UI
st.set_page_config(page_title="LLM App", layout="centered")

st.title("🧠 LangChain App (OpenAI + LLaMA 3.2)")

# Task selector
task = st.selectbox(
    "Choose what you want to generate:",
    ["Essay (OpenAI)", "Poem (LLaMA 3.2 - Local)"]
)

# Input
user_input = st.text_input("Enter your topic:")

# Chat display
if user_input:
    st.chat_message("user").write(user_input)

    with st.spinner("Thinking..."):
        if task == "Essay (OpenAI)":
            result = call_api(
                "/essay/invoke",
                {"input": {"topic": user_input}}
            )
        else:
            result = call_api(
                "/poem/invoke",
                {"input": {"topic": user_input}}
            )

    st.chat_message("assistant").write(result)