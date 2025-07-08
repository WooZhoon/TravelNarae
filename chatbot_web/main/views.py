from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from dotenv import load_dotenv
import json
import sys
import os

load_dotenv()
TOUR_API_KEY = os.getenv("TOUR_API_KEY")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from langchain_core.messages import HumanMessage
from chat_agent import agent, generate_config
from llm_tools.chat_history_manager import chat_store
# ===== 기본 페이지 뷰 =====
def index(request):
    return render(request, 'main/index.html')

def chatbot(request):
    session_id = get_session_id(request)
    messages = chat_store.get_messages(session_id)

    frontend_msgs = [
        {"sender": "user" if isinstance(m, HumanMessage) else "bot", "text": m.content}
        for m in messages
    ]

    return render(request, 'main/chatbot.html', {
        "messages": frontend_msgs,
        "session_id": session_id,
    })

def board(request):
    return render(request, 'main/board.html')

def profile(request):
    return render(request, 'main/profile.html')

# ===== 로그인 =====
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # 핵심: 로그인 세션 생성
            return redirect('main:home')
        else:
            return render(request, 'main/login.html', {'error': "Invalid username or password."})

    return render(request, 'main/login.html')

# ===== 로그아웃 =====
def logout_request(request):
    logout(request)  # 세션 및 인증 정보 모두 제거
    return redirect('main:home')

# ===== 회원가입 =====
# (web_signup이 User 모델과 연동되어 있다고 가정)
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        nickname = request.POST.get('nickname')

        if password != password2:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return render(request, 'main/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "이미 존재하는 아이디입니다.")
            return render(request, 'main/signup.html')

        user = User.objects.create_user(username=username, password=password)
        # User 모델에 nickname 필드가 없으면, UserProfile 같은 별도 모델 만들어서 처리하는 게 정석임
        # 여기서는 그냥 임시로 first_name에 저장해보자 (닉네임 용도)
        user.first_name = nickname
        user.save()

        login(request, user)  # 회원가입 후 자동 로그인
        return redirect('main:home')

    return render(request, 'main/signup.html')

# ===== 세션 ID 획득 =====
def get_session_id(request):
    if request.user.is_authenticated:
        return request.user.username
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

# ===== 챗봇 응답 처리 =====
def chatbot_response(request, user_message):
    session_id = get_session_id(request)
    app = agent()
    config = generate_config(session_id)

    state = {
        "session_id": session_id,
        "messages": [HumanMessage(content=user_message)]
    }

    try:
        response = app.invoke(state, config=config)
        last_msg = response["messages"][-1].content
        return last_msg
    except Exception as e:
        return f"챗봇 오류 발생: {e}"

# ===== API (AJAX용) =====
@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_msg = data.get("message", "")
            reply = chatbot_response(request, user_msg)
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"error": f"요청 처리 오류: {str(e)}"}, status=500)
    return JsonResponse({"error": "POST 요청만 허용"}, status=405)