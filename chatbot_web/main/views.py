
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.shortcuts import render
from django.conf import settings
import requests
import json
import sys
import os


load_dotenv()
TOUR_API_KEY = os.getenv("TOUR_API_KEY")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from auth import web_login as custom_login, web_signup
# from chat_agent import agent, generate_config
# from langchain_core.messages import HumanMessage

def index(request):
    return render(request, 'main/index.html')

def chatbot(request):
    return render(request, 'main/chatbot.html')

def board(request):
    return render(request, 'main/board.html')

def login_view(request):
    return render(request, 'main/login.html')  #Login UI 확인용 / 아래 주석부분 대체

def signup(request):
    return render(request, 'main/signup.html') #Signup UI 확인용 / 아래 주석부분 대체

def recommendation(request):
    return render(request, 'main/recommended.html', {
        'TOUR_API_KEY': os.getenv("TOUR_API_KEY")
    })

def map_view(request):
    return render(request, 'main/heritage_map.html')  # 아직 구현 안 됐음




# def login_view(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('username')
#         user_pw = request.POST.get('password')
        
#         nickname = custom_login(user_id, user_pw)
        
#         if nickname:
#             request.session['nickname'] = nickname
#             return redirect('main:home')
#         else:
#             error_message = "Invalid username or password."
#             return render(request, 'main/login.html', {'error': error_message})
            
#     return render(request, 'main/login.html')

# def logout_request(request):
#     if 'nickname' in request.session:
#         del request.session['nickname']
#     return redirect("main:home")

# def signup(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('username')
#         user_pw = request.POST.get('password')
        
#         if web_signup(user_id, user_pw):
#             return redirect('main:login')
#         else:
#             error_message = "Username already exists."
#             return render(request, 'main/signup.html', {'error': error_message})
            
#     return render(request, 'main/signup.html')

# def chatbot_response(request, user_message):
#     session_id = request.session.get('nickname', 'anonymous') # 로그인된 사용자 닉네임 사용, 없으면 anonymous
#     app = agent()
#     config = generate_config(session_id)

#     state = {
#         "session_id": session_id,
#         "messages": [HumanMessage(content=user_message)]
#     }

#     try:
#         response = app.invoke(state, config=config)
#         last_msg = response["messages"][-1].content
#         return last_msg
#     except Exception as e:
#         return f"챗봇 오류 발생: {e}"

# def profile(request):
#     return render(request, 'main/profile.html')

# @csrf_exempt  
# def chat_api(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         user_msg = data.get("message", "")
#         reply = chatbot_response(request, user_msg)
#         return JsonResponse({"reply": reply})
#     return JsonResponse({"error": "POST 요청만 허용"}, status=405)


