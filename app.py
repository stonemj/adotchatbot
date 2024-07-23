import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 설정
client = OpenAI(api_key="sk-proj-cJVaChZSqWtXbeeEvYsmT3BlbkFJcHuWohCWEkCPnx5nqzNd")

# 어시스턴트 ID
ASSISTANT_ID = "asst_kSpI6lSV52HpMJczFXXPuGyT"

# Streamlit 앱 제목 설정
st.title("에이닷 물어보삼")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력 받기
user_input = st.text_input("질문을 입력하세요:")

# 메시지 전송 버튼
if st.button("전송"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI API를 사용하여 응답 생성
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 다른 적절한 모델
        messages=[
            {"role": "system", "content": "당신은 에이닷 물어보삼이라는 이름의 유용한 어시스턴트입니다."},
            *st.session_state.messages
        ]
    )

    # 어시스턴트 응답 추가
    assistant_response = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# 대화 내용 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("사용자:", value=message["content"], height=100, disabled=True)
    else:
        st.text_area("에이닷 물어보삼:", value=message["content"], height=100, disabled=True)
