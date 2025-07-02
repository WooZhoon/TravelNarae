########## chat_history_manager.py
"""
agent와 나눈 대화 내역을 저장하는 manager 파일입니다.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.chat_message_histories import SQLChatMessageHistory

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
DB = os.getenv("DB")

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")
# engine = create_engine(f"mysql+pymysql://root:password@localhost:3306/{DB}")

class ChatHistoryManager:
    def __init__(self):
        self.engine = engine
        self.store = {}  # ❗ optional cache
        
    def get_session_history(self, session_id: str) -> SQLChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = SQLChatMessageHistory(
                session_id=session_id,
                connection=self.engine
            )
            
        return self.store[session_id]
    
    def get_cached_messages(self, session_id: str):
        if session_id not in self.memory_cache:
            # ✅ 최초엔 DB에서 불러와서 메모리에 올린다
            history = self.get_session_history(session_id)
            self.memory_cache[session_id] = history.messages
        return self.memory_cache[session_id]

    def append_message(self, session_id: str, msg):
        self.get_cached_messages(session_id).append(msg)

    def flush_to_db(self, session_id: str):
        if session_id in self.memory_cache:
            history = self.get_session_history(session_id)
            history.clear()
            for m in self.memory_cache[session_id]:
                history.add_message(m)