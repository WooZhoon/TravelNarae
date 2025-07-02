from chat_agent import agent, generate_config

def main():
    app = agent()
    session_id = input(">>> session id를 입력하세요: ")
    config = generate_config(session_id)

    while True:
        query = input(">>> 쿼리를 입력하세요: ")
        if query == "!quit" or query == "!벼ㅑㅅ":
            break
        response = app.invoke(
            {"messages":query},
            config=config)

        print(f"\n{response["messages"][1].content}\n")

main()