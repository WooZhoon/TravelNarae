
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'index.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def board(request):
    return render(request, 'board.html')

def login_view(request):
    return render(request, 'login.html')



def chatbot_response(user_message):
    return f"챗봇이 응답한 메시지: {user_message}"

@csrf_exempt  
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "")
        reply = chatbot_response(user_msg)
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "POST 요청만 허용"}, status=405)


