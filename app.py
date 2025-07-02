from chat_agent import agent,config

def main():
    app = agent()

    while True:
        query = input(">>> 쿼리를 입력하세요:")
        if query == "!quit" or query == "!벼ㅑㅅ":
            break
        response = app.invoke(
            {"messege":query},
            config=config)

        print(f"\n{response}\n")

main()