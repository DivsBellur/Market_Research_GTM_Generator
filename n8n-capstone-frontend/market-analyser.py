import streamlit as st
import requests
import uuid

N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/abc123-chat"

st.title("Your go-to-market AI Agent")

# Persist a session ID for this browser session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Which market topic would you like to research and develop a go-to-market strategy for? "):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking...strategizing..."):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "chatInput": prompt,
                    "sessionId": st.session_state.session_id
                },
                timeout=120
            )
            data = response.json()
            # n8n's Chat Trigger typically returns {"output": "..."} 
            reply = data.get("output", str(data))
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})