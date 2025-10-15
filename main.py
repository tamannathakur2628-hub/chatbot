import streamlit as st
from google.genai import Client
from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = Client(api_key=GEMINI_API_KEY)
st.set_page_config(page_title="NHAI Smart Assistant", page_icon="🚧", layout="centered")
st.title("🚦 NHAI Smart Assistant")
st.caption("Helping passengers with FASTag, tolls, highways, and NHAI info.")

# system prompt for NHAI chatbot
system_prompt = """
You are an AI assistant for the National Highways Authority of India (NHAI).
Answer politely and factually. If unsure, guide the user to helpline 1033 or https://nhai.gov.in.
"""

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Hi! I’m the NHAI Assistant. How can I help you today?"}
    ]

# user input
user_input = st.chat_input("Ask about FASTag, tolls, complaints, or highways...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# display chat
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
