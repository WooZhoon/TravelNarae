# 로그인 및 회원가입 선택
## 로그인 선택시 id, 비번 입력
## id로 DB에서 찾고, (입력한 비번을 암호화 한 거) 랑 (저장된 암호화된 비번) 이랑 비교.
### 같으면 성공 -> query 입력 단계로
### 다르면 실패 -> 로그인 단계로

## 회원가입 선택시, id 입력 후 중복검사
### 같은게 있으면? 다시 입력.
### 없으면? 사용가능한 아이디입니다.

### 비밀번호 입력시 -> 조건을 만족하면 유효한 비밀번호입니다.
###                -> 조건을 만족하지 않으면? 만족 못한 조건 ex: 비밀번호가 너무 짧습니다.

### 입력한 비밀번호랑 비밀번호 확인란이랑 비교
import bcrypt
from create_engine import engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# 비밀번호 해시 생성
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# 비밀번호 검증
def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# 회원가입 함수
def sign_up():
    db = SessionLocal()
    while True:
        username = input(">>> 아이디를 입력하세요: ").strip()
        if db.query(User).filter_by(username=username).first():
            print("이미 존재하는 아이디입니다.")
        else:
            print("사용 가능한 아이디입니다.")
            break

    while True:
        password = input(">>> 비밀번호를 입력하세요: ").strip()
        confirm = input(">>> 비밀번호를 다시 입력하세요: ").strip()

        if password != confirm:
            print("비밀번호가 일치하지 않습니다.")
            continue
        if len(password) < 8:
            print("비밀번호가 너무 짧습니다.")
            continue
        break

    hashed_pw = hash_password(password)
    new_user = User(username=username, password_hash=hashed_pw.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.close()
    print("회원가입 성공!")

# 로그인 함수
def sign_in():
    db = SessionLocal()
    username = input(">>> 아이디를 입력하세요: ").strip()
    password = input(">>> 비밀번호를 입력하세요: ").strip()

    user = db.query(User).filter_by(username=username).first()
    db.close()

    if not user:
        print("존재하지 않는 아이디입니다.")
        return None

    if check_password(password, user.password_hash.encode('utf-8')):
        print("로그인 성공!")
        return username
    else:
        print("비밀번호가 틀렸습니다.")
        return None

# Base.metadata.create_all(engine)  # 테이블 처음 생성할 때만 실행
