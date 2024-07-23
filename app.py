import streamlit as st
import openai
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
openai.api_key = api_key

# Streamlit 앱 구성
st.title("AI Assistant Chat")

# 채팅 기록을 저장할 리스트
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def chat_with_assistant(user_input):
    try:
        # OpenAI API를 사용하여 응답 생성
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        assistant_response = response.choices[0].text.strip()
        return assistant_response
    except Exception as e:
        st.error(f"Failed to communicate with the assistant: {e}")
        return "Sorry, there was an error processing your request."

# 사용자 입력 처리
prompt = st.text_input("What is your question?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답
    with st.chat_message("assistant"):
        response = chat_with_assistant(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
