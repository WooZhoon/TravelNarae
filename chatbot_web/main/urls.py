from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('board/', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    path('api/chat/', views.chat_api, name='chat_api'),
]