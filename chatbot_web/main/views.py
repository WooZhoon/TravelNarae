
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'main/index.html')

def chatbot(request):
    return render(request, 'main/chatbot.html')

def board(request):
    return render(request, 'main/board.html')

def login_view(request):
    return render(request, 'main/login.html')



def chatbot_response(user_message):
    return f"챗봇이 응답한 메시지: {user_message}"


def profile(request):
    return render(request, 'main/profile.html')

@csrf_exempt  
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "")
        reply = chatbot_response(user_msg)
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "POST 요청만 허용"}, status=405)


