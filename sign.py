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
from sqlalchemy import text

conn = engine().connect()

# 비밀번호 해시 생성
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# 비밀번호 검증
def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# 로그인 함수
def Sign_In():
    username = input(">>> 아이디를 입력하세요: ").strip()
    password = input(">>> 암호를 입력하세요: ").strip()

    query = text("SELECT password_hash FROM test_userDB WHERE username = :username")
    result = conn.execute(query, {"username": username}).fetchone()

    if result is None:
        print("존재하지 않는 아이디입니다.")
        return False

    stored_hash = result[0].encode('utf-8')

    if check_password(password, stored_hash):
        print("로그인 성공!")
        return True
    else:
        print("비밀번호가 틀렸습니다.")
        return False

# 회원가입 함수
def Sign_Up():
    while True:
        username = input(">>> 아이디를 입력하세요: ").strip()

        # 중복 검사
        query = text("SELECT 1 FROM test_userDB WHERE username = :username")
        if conn.execute(query, {"username": username}).fetchone():
            print("이미 존재하는 아이디입니다. 다시 입력하세요.")
        else:
            print("사용 가능한 아이디입니다.")
            break

    while True:
        password = input(">>> 비밀번호를 입력하세요: ").strip()
        password_confirm = input(">>> 비밀번호를 한 번 더 입력하세요: ").strip()

        if password != password_confirm:
            print("비밀번호가 일치하지 않습니다. 다시 입력하세요.")
            continue

        # 비밀번호 유효성 검사 (예: 최소 8자 이상)
        if len(password) < 8:
            print("비밀번호가 너무 짧습니다. 최소 8자 이상이어야 합니다.")
            continue

        # 여기에 더 복잡한 조건 추가 가능 (특수문자, 대문자 등)
        break

    hashed_pw = hash_password(password)

    # DB 저장
    insert_query = text(
        "INSERT INTO test_userDB (username, password_hash) VALUES (:username, :password_hash)"
    )
    conn.execute(insert_query, {"username": username, "password_hash": hashed_pw.decode('utf-8')})
    conn.commit()

    print("회원가입 성공!")

