import streamlit as st
from groq import Groq

GROQ_API_KEY = "your_groq_api_key_here"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="NHAI Smart Assistant",layout="centered")
st.title("🚦 NHAI Smart Assistant")
st.caption("Get help with FASTag, tolls, highways, and NHAI-related issues.")

system_prompt = """
You are an assistant for the National Highways Authority of India (NHAI).
Be polite and factual. If unsure, guide the user to helpline 1033 or https://nhai.gov.in.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Hi! I’m the NHAI Assistant. How can I help you today?"}
    ]

user_input = st.chat_input("Ask about FASTag, tolls, or complaints...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
