import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable in your .env file.")
    st.stop()

# OpenAI 클라이언트 설정
client = OpenAI(api_key=api_key)

# Streamlit 앱 구성
st.title("AI Assistant Chat (GPT-3.5 Turbo)")

# 채팅 기록을 저장할 리스트
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def chat_with_assistant(messages):
    try:
        # OpenAI API를 사용하여 응답 생성 (GPT-3.5 Turbo 사용)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Failed to communicate with the assistant: {e}")
        return "Sorry, there was an error processing your request."

# 사용자 입력 처리
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    response = chat_with_assistant(messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)