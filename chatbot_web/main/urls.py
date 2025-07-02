from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('board/', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='home'), name="logout"),
    path("profile/", views.profile, name="profile"),
]