import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="NHAI Smart Assistant", page_icon="🚧", layout="centered")
st.title("🚦 NHAI Smart Assistant")
st.caption("Helping passengers with FASTag, tolls, highways, and NHAI info.")

system_prompt_text = """
You are an AI assistant for the National Highways Authority of India (NHAI).
Answer politely and factually. If unsure, guide the user to helpline 1033 or https://nhai.gov.in.
"""

model = genai.GenerativeModel('gemini-2.5-flash')

if "chat" not in st.session_state:
    initial_history_for_gemini = [
        {"role": "user", "parts": [system_prompt_text]},
        {"role": "model", "parts": ["Understood. I am ready to assist as the NHAI Assistant."]}
    ]
    st.session_state.chat = model.start_chat(history=initial_history_for_gemini)

    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I’m the NHAI Assistant. How can I help you today?"}
    ]

user_input = st.chat_input("Ask about FASTag, tolls, complaints, or highways...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = st.session_state.chat.send_message(user_input)
        reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process that request right now. Please try again or contact helpline 1033."})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
