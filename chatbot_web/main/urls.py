from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('board/', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    # path('api/chat/', views.chat_api, name='chat_api'),
    # path("logout/", views.logout_request, name="logout"),
    # path("profile/", views.profile, name="profile"),
    path('signup/', views.signup, name='signup'),
    path('recommendation/', views.recommendation, name='recommendation'),  # 임시
    path('map/', views.map_view, name='map'),
]