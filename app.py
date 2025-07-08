import logging
from chat_agent import agent, generate_config
from langchain_core.messages import HumanMessage
from auth import sign_in, sign_up  # ✅ 회원가입/로그인 함수가 여기에 정의되어 있다고 가정
from dotenv import load_dotenv
load_dotenv()

logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    print("\n🧠 Cultural Agent에 오신 것을 환영합니다.\n")

    while True:
        choice = input("1. 로그인\n2. 회원가입\n선택하세요 (1 or 2): ").strip()
        if choice == "1":
            username = sign_in()
            if username:
                break
        elif choice == "2":
            sign_up()
        else:
            print("⚠️ 잘못된 입력입니다. 1 또는 2를 선택하세요.")

    session_id = username  # ✅ username이 곧 세션 ID

    app = agent()
    config = generate_config(session_id)

    while True:
        query = input("\n>>> 쿼리를 입력하세요 (!quit 입력 시 종료): ").strip()
        if query in ("!quit", "!벼ㅑㅅ"):
            print("👋 세션을 종료합니다.")
            break
        if not query:
            continue

        state = {
            "session_id": session_id,
            "messages": [HumanMessage(content=query)]
        }

        try:
            response = app.invoke(state, config=config)
            last_msg = response["messages"][-1].content
            print(f"\n🧠 {last_msg}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
