from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# OpenAI 클라이언트 생성
client = OpenAI(api_key="sk-proj-ZfhEAvI5zLQpFjWSn6nST3BlbkFJNoP5l2Es4jNOuvrngnb1")

# 어시스턴트 ID
assistant_id = "asst_kSpI6lSV52HpMJczFXXPuGyT"

# 새 스레드 생성
thread = client.beta.threads.create()

def chat_with_assistant(user_input):
    # 사용자 메시지를 스레드에 추가
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # 어시스턴트에게 실행 요청
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # 실행 완료 대기
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # 어시스턴트의 응답 가져오기
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    return assistant_response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = chat_with_assistant(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)