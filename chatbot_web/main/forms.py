from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    author_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '이름'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '내용을 입력하세요', 'rows': 3}))

    class Meta:
        model = Comment
        fields = ['author_name', 'password', 'content']