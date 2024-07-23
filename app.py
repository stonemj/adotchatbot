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

# OpenAI 클라이언트 생성
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {e}")
    st.stop()

# 어시스턴트 ID
assistant_id = "asst_kSpI6lSV52HpMJczFXXPuGyT"

# 세션 상태에 스레드 ID 저장
if "thread_id" not in st.session_state:
    try:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    except Exception as e:
        st.error(f"Failed to create thread: {e}")
        st.stop()

def chat_with_assistant(user_input):
    try:
        # 사용자 메시지를 스레드에 추가
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_input
        )

        # 어시스턴트에게 실행 요청
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )

        # 실행 완료 대기
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=st.session_state.thread_id, run_id=run.id)

        # 어시스턴트의 응답 가져오기
        messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
        assistant_response = messages.data[0].content[0].text.value

        return assistant_response
    except Exception as e:
        st.error(f"Failed to communicate with the assistant: {e}")
        return "Sorry, there was an error processing your request."

# Streamlit 앱 구성
st.title("AI Assistant Chat")

# 채팅 기록을 저장할 리스트
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답
    with st.chat_message("assistant"):
        response = chat_with_assistant(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
