# -*- coding: utf-8 -*-
import bcrypt
import getpass
from create_engine import engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# DB 연결
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM 모델 정의
class User(Base):
    __tablename__ = "test_userDB"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50), default="")

# --- Core Logic (Database Interaction) ---

def hash_password(password: str) -> bytes:
    """비밀번호를 해시화합니다."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    """입력된 비밀번호와 해시된 비밀번호를 비교합니다."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def get_user(db: Session, username: str) -> User | None:
    """사용자 이름으로 사용자를 조회합니다."""
    return db.query(User).filter_by(username=username).first()

def create_user(db: Session, username: str, password: str) -> User:
    """새로운 사용자를 생성하고 데이터베이스에 추가합니다."""
    hashed_pw = hash_password(password)
    new_user = User(username=username, password_hash=hashed_pw.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- UI Logic (Command-Line Interaction) ---

def sign_up():
    """사용자 회원가입을 처리하는 UI 함수입니다."""
    db = SessionLocal()
    try:
        # 아이디 입력 및 중복 검사
        while True:
            username = input(">>> 아이디를 입력하세요: ").strip()
            if not get_user(db, username):
                print("사용 가능한 아이디입니다.")
                break
            else:
                print("이미 존재하는 아이디입니다.")

        # 비밀번호 입력 및 확인
        while True:
            password = getpass.getpass(">>> 비밀번호를 입력하세요 (8자 이상): ").strip()
            if len(password) < 8:
                print("비밀번호가 너무 짧습니다. 8자 이상 입력해주세요.")
                continue

            confirm = getpass.getpass(">>> 비밀번호를 다시 입력하세요: ").strip()
            if password == confirm:
                break
            else:
                print("비밀번호가 일치하지 않습니다.")

        # 사용자 생성
        create_user(db, username, password)
        print("회원가입 성공!")

    finally:
        db.close()


def sign_in():
    """사용자 로그인을 처리하는 UI 함수입니다."""
    db = SessionLocal()
    try:
        username = input(">>> 아이디를 입력하세요: ").strip()
        password = getpass.getpass(">>> 비밀번호를 입력하세요: ").strip()

        user = get_user(db, username)

        if user and check_password(password, user.password_hash.encode('utf-8')):
            print("로그인 성공!")
            return username
        else:
            print("아이디 또는 비밀번호가 틀렸습니다.")
            return None
    finally:
        db.close()

# Base.metadata.create_all(engine)  # 테이블 처음 생성할 때만 실행