# 🔧 기본 Django 라이브러리
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# 🔧 파이썬 표준 라이브러리
import json
import sys
import os

# 🔧 로컬 모델
from .models import ChatSession, ChatMessage

# 🔧 시스템 경로 등록
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 🔧 외부 모듈 (LangChain 기반 응답 생성)
from langchain_core.messages import HumanMessage
from chat_agent import agent, generate_config
from llm_tools.chat_history_manager import chat_store

# ===================================================
# 🌐 일반 페이지 뷰
# ===================================================

def index(request):
    return render(request, 'main/index.html')


def board(request):
    return render(request, 'main/board.html')


def profile(request):
    return render(request, 'main/profile.html')

# ===================================================
# 🔐 사용자 인증
# ===================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('main:home')
        else:
            return render(request, 'main/login.html', {'error': "Invalid username or password."})

    return render(request, 'main/login.html')


def logout_request(request):
    logout(request)
    return redirect('main:home')


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
        user.first_name = nickname  # 임시 닉네임 저장
        user.save()

        login(request, user)
        return redirect('main:home')

    return render(request, 'main/signup.html')

# ===================================================
# 💬 채팅 시스템: 페이지 + 대화 처리
# ===================================================

@login_required
def chatbot(request):
    # 새로운 채팅 세션을 생성하고 해당 페이지로 이동
    session = ChatSession.objects.create(user=request.user, title="새 채팅")
    return redirect('main:chat_bot', session_id=session.id)


@login_required
def chatbot_redirect_to_latest_session(request):
    # 현재 사용자의 가장 최근 채팅 세션을 찾음
    latest_session = ChatSession.objects.filter(user=request.user).order_by('-created_at').first()

    if latest_session:
        # 가장 최근 세션으로 리디렉션
        return redirect('main:chat_bot', session_id=latest_session.id)
    else:
        # 채팅 세션이 없으면 새로 만들어서 해당 세션으로 이동
        return chatbot(request)


@login_required
def chat_bot_view(request, session_id):
    user = request.user
    sessions = ChatSession.objects.filter(user=user).order_by('-created_at')
    selected_session = get_object_or_404(ChatSession, id=session_id, user=user)
    messages = selected_session.messages.order_by('timestamp')

    return render(request, 'main/chatbot.html', {
        'sessions': sessions,
        'selected_session': selected_session,
        'messages': messages,
    })

# ===================================================
# ⚙️ 유틸리티 함수: 세션 ID, 챗봇 응답
# ===================================================

def get_session_id(request):
    # 인증된 유저의 고유 세션 키를 가져옴
    if request.user.is_authenticated:
        return request.user.username
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def chatbot_response(request, user_message):
    # LangChain 기반 챗봇 응답 생성
    session_id = get_session_id(request)
    app = agent()
    config = generate_config(session_id)
    state = {"session_id": session_id, "messages": [HumanMessage(content=user_message)]}

    try:
        response = app.invoke(state, config=config)
        return response["messages"][-1].content
    except Exception as e:
        return f"챗봇 오류 발생: {e}"

# ===================================================
# 🔄 비동기 API (AJAX 기반)
# ===================================================

@csrf_exempt
@login_required
def chat_api(request):
    # 비동기 POST 요청으로 챗봇 응답 생성 및 DB 저장
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 허용"}, status=405)

    try:
        data = json.loads(request.body)
        user_msg = data.get("message", "")

        # 최신 채팅 세션 가져오기
        session = ChatSession.objects.filter(user=request.user).order_by('-created_at').first()
        if not session:
            session = ChatSession.objects.create(user=request.user, title="비동기 채팅")

        # 유저 메시지 저장
        ChatMessage.objects.create(session=session, role='user', content=user_msg)

        # AI 응답 생성
        reply = chatbot_response(request, user_msg)

        # AI 메시지 저장
        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({"error": f"요청 처리 오류: {str(e)}"}, status=500)
