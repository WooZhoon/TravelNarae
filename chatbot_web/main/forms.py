from django import forms
from .models import Comment
from django.contrib.auth.models import User

class UserChangeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '닉네임'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}))

    class Meta:
        model = User
        fields = ['first_name', 'email']

class CommentForm(forms.ModelForm):
    author_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '이름'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '내용을 입력하세요', 'rows': 3}))

    class Meta:
        model = Comment
        fields = ['author_name', 'password', 'content']