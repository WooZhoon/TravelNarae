# discord_agent.py
import os
import discord
import traceback
from chat_agent import agent, generate_config
from langchain_core.messages import HumanMessage

# --- 초기 설정 ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
app = agent()
flag = False

# --- 디스코드 클라이언트 설정 ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- LangChain 응답 처리 함수 ---
async def generate_response(prompt: str, session_id: str) -> str:
    try:
        config = generate_config(session_id)
        state = {
            "session_id": session_id,
            "messages": [HumanMessage(content=prompt)],
        }

        response = app.invoke(state, config)
        return response["messages"][-1].content

    except Exception:
        traceback.print_exc()
        return "기가차드가 잠깐 쓰러졌어... 다시 시도해봐."

# --- 메시지 분할 전송 함수 ---
async def send_by_paragraph_chunk(channel, text, max_chunk_len=1800):
    paragraphs = text.split('\n\n')
    chunk = ""
    for para in paragraphs:
        if len(chunk) + len(para) + 2 > max_chunk_len:
            await channel.send(chunk.strip())
            chunk = ""
        chunk += para + "\n"
    if chunk.strip():
        await channel.send(chunk.strip())

# --- 디스코드 이벤트 핸들링 ---
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.offline)
    print("기가차드가 잠시 잠든 상태로 대기 중이다...")

@client.event
async def on_message(message):
    global flag
    if message.author.bot:
        return

    content = message.content.strip()

    # 봇 활성화 키워드
    if "기가차드" in content.lower() and not flag:
        flag = True
        await client.change_presence(status=discord.Status.online)
        await message.channel.send("날 불렀나, My son.")
        return

    # 상태 확인
    if content.lower() == "!flag":
        await message.channel.send(f"현재 상태: {'활성화' if flag else '비활성화'}")
        return

    # 도움말
    if content.lower() == "!help":
        help_msg = (
            "**기가차드 사용법**\n"
            "- `기가차드` 라고 말하면 깨어난다\n"
            "- 질문을 던지면 답해준다\n"
            "- `!off` → 다시 잠든다\n"
            "- `!help` → 이 도움말 출력\n"
        )
        await message.channel.send(help_msg)
        return

    # 봇 비활성화
    if content.lower() == "!off":
        flag = False
        await client.change_presence(status=discord.Status.offline)
        await message.channel.send("잘 있어라, My son.")
        return

    # 메시지 처리
    if flag:
        session_id = f"{message.guild.id}_{message.author.id}" if message.guild else str(message.author.id)
        response = await generate_response(content, session_id)
        await send_by_paragraph_chunk(message.channel, response)

# --- 봇 실행 ---
client.run(DISCORD_TOKEN)
