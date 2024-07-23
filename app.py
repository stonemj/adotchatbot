import streamlit as st
import openai
import time

# Streamlit 비밀 정보에서 API 키 가져오기
api_key = st.secrets["openai"]["api_key"]
if not api_key:
    st.error("API key not found. Please set the API key in the secrets.toml file.")
    st.stop()

# OpenAI 클라이언트 설정
openai.api_key = api_key

# 어시스턴트 ID
assistant_id = "gpt-3.5-turbo"

# Streamlit 앱 구성
st.title("AI Assistant Chat")

# 세션 상태에 스레드 ID 저장
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# 채팅 기록을 저장할 리스트
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def chat_with_assistant(user_input):
    try:
        # 사용자 메시지를 스레드에 추가
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 어시스턴트의 응답 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.messages
            ]
        )

        assistant_response = response.choices[0].message["content"].strip()

        # 어시스턴트의 응답을 세션 상태에 추가
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        return assistant_response
    except Exception as e:
        st.error(f"Failed to communicate with the assistant: {e}")
        return "Sorry, there was an error processing your request."

# 사용자 입력 처리
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답
    response = chat_with_assistant(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
