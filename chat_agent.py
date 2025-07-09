# # ✅ LangGraph 기반으로 리팩토링된 agent.py

# # 🌐 기본 라이브러리
# import os
# from typing import TypedDict, Annotated
# from dotenv import load_dotenv

# # 🤖 LangChain 관련
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
# from langchain_core.runnables import RunnableConfig

# # 🧠 LangGraph 관련
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode, tools_condition
# from langgraph.checkpoint.memory import MemorySaver

# 🛠️ 사용자 정의 도구
from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from llm_tools.google_places import get_places_by_keyword_and_location
from llm_tools.naver_search import NaverSearchTool
from llm_tools.chat_history_manager import chat_store

# # 🧾 프롬프트
# from system_prompt import get_system_prompt

# # ✅ 환경 변수 로드
# load_dotenv()

# ✅ 상태 저장소
memory = MemorySaver()

# # ✅ 상태 정의
# class State(TypedDict):
#     session_id: str
#     messages: Annotated[list, add_messages]


# # ✅ Config 생성 함수
# def generate_config(session_id: str) -> RunnableConfig:
#     return RunnableConfig(
#         recursion_limit=10,
#         configurable={"thread_id": session_id},
#         tags=["my-tag"]
#     )


# # ✅ System Prompt 삽입 노드
# def prompt_node(state: State) -> State:
#     system_msg = SystemMessage(content=get_system_prompt())
#     if not any(msg.type == "system" for msg in state["messages"]):
#         state["messages"] = [system_msg] + state["messages"]
#     return state


# # ✅ ChatBot 노드 (LLM 호출 + DB 저장)
# def build_chatbot_node(tools):
#     llm = ChatOpenAI(model_name='gpt-4.1')
#     llm_with_tools = llm.bind_tools(tools)

#     # LLM에 전달할 최대 메시지 수
#     MAX_HISTORY_MESSAGES = 10 # 필요에 따라 이 값을 조정하세요.

    def chatbot(state: State) -> State:
        # 사용자 메시지도 저장
        user_msg = next((msg for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)), None)
        if user_msg:
            chat_store.append_message(state["session_id"], user_msg)

        # 최근 메시지만 LLM에 전달
        messages_to_send = state["messages"][-MAX_HISTORY_MESSAGES:]
        response = llm_with_tools.invoke(messages_to_send)

        # 메시지 저장은 append_message로 통일
        chat_store.append_message(state["session_id"], response)

        # 최신 메시지 목록 반환 (DB/캐시 기준)
        latest_msgs = chat_store.get_messages(state["session_id"])

        return {
            "session_id": state["session_id"],
            "messages": latest_msgs,
        }

#     return chatbot


# # ✅ 에이전트 그래프 정의 함수
# def agent():
#     # 도구 정의
#     naver = NaverSearchTool()
#     tools = [RAG_tool, get_weather_by_location_and_date, naver]

#     # LangGraph 정의
#     graph = StateGraph(State)

#     # 노드 등록
#     graph.add_node("prompt", prompt_node)
#     graph.add_node("chatbot", build_chatbot_node(tools))
#     graph.add_node("tools", ToolNode(tools=tools))

#     # 노드 연결
#     graph.add_edge(START, "prompt")
#     graph.add_edge("prompt", "chatbot")
#     graph.add_conditional_edges("chatbot", tools_condition)
#     graph.add_edge("tools", "chatbot")
#     graph.add_edge("chatbot", END)

#     return graph.compile(checkpointer=memory)
