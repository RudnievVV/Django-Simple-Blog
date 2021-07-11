from django import forms
from captcha.fields import CaptchaField
from .models import Post, Comment


class PostForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ['user_name', 'title', 'email', 'home_page', 'text', 'captcha']


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['user_name', 'title', 'email', 'home_page', 'text', 'captcha']