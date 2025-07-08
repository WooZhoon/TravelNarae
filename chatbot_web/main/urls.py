from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot_redirect_to_latest_session, name='chatbot'),
    path('chatbot/new/', views.chatbot, name='chatbot_new'),
    path('board/', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path('signup/', views.signup, name='signup'),
    path('chatbot/<int:session_id>/', views.chat_bot_view, name='chat_bot'),
]