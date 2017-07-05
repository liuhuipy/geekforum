__author__ = 'liuhui'


from django import forms
from django.contrib import auth
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名', widget=forms.TextInput(attrs={'placeholder': '用户名或邮箱', 'required': 'required'}), max_length=32, error_messages={'required': u'用户名或邮箱不能为空!'})
    password = forms.CharField(label=u'密码',  widget=forms.PasswordInput(attrs={'placeholder': '密码', 'required': 'required'}), max_length=16, error_messages={'required': u'密码不能为空！'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'用户名或密码不匹配')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    res_password = forms.CharField()

