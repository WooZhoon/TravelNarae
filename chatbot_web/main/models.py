from django.db import models
from django.contrib.auth.models import User  # ✅ 이거 추가해야 User 외래키 연결됨

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 누가 만든 쪽지함인지
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:30]}"
