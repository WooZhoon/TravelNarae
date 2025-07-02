import logging
from chat_agent import agent, generate_config
from langchain_core.messages import HumanMessage

logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    session_id = input(">>> session id를 입력하세요: ")
    app = agent(session_id)  # ✅ agent가 session_id 받아서 ChatHistory도 세팅하게끔!
    config = generate_config(session_id)

    while True:
        query = input(">>> 쿼리를 입력하세요: ")
        if query in ("!quit", "!벼ㅑㅅ"):
            break

        # ✅ 올바른 메시지 형식으로 전달
        state = {
            "session_id": session_id,  # ✅ state에 포함되도록 State 구조 수정 필요
            "messages": [HumanMessage(content=query)]
        }

        response = app.invoke(state, config=config)

        # ✅ 응답 메시지 추출 (마지막 메시지 content)
        last_msg = response["messages"][-1].content
        print(f"\n🧠 {last_msg}\n")

main()
