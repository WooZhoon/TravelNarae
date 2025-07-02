# ✅ LangGraph 기반으로 리팩토링된 agent.py

from dotenv import load_dotenv
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from typing import Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from llm_tools.google_places import get_places_by_keyword_and_location
from llm_tools.naver_search import NaverSearchTool
from langgraph.graph.message import add_messages

load_dotenv()
memory = MemorySaver()
from langchain_core.runnables import RunnableConfig
config = RunnableConfig(
    recursion_limit=10,
    configurable={"thread_id": "1"},
    tags=["my-tag"])

# ✅ 상태 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent():
    tools = [NaverSearchTool(),RAG_tool,get_weather_by_location_and_date]
    # print("🔧 Tools:", tools)

    llm = ChatOpenAI(model_name='gpt-4.1')
    llm_with_tools = llm.bind_tools(tools)

    # 챗봇 노드 정의
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # 상태 그래프 정의
    graph_builder = StateGraph(State)

    # 노드 구성
    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")

    # 시작과 종료 정의
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    # 그래프 컴파일
    return graph_builder.compile(checkpointer=memory)
    