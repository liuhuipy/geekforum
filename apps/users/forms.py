#coding:utf8
__author__ = 'liuhui'

import random

from django import forms
from django.contrib import auth
from .models import UserProfile

from django.utils import timezone

error_messages = {
    'username': {
        'required': u'用户名不能为空',
        'min_length': u'用户名长度过短（4-16个字符）',
        'max_length': u'用户名长度过长（4-16个字符）',
        'invalid': u'用户名必须由英文(开头)，数字，下划线构成',
    },
    'email': {
        'required': u'E-mail不能为空',
        'min_length': u'Email长度过短',
        'max_length': u'Email长度过长',
        'invalid': u'电子邮件格式不正确',
    },
    'password': {
        'required': u'密码不能为空',
        'min_length': u'密码长度过短（6-16个字符）',
        'max_length': u'密码长度过长（6-16个字符）',
    }
}



class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名', min_length=4, max_length=32, error_messages=error_messages.get('username'))
    password = forms.CharField(label=u'密码', min_length=6, max_length=16, error_messages=error_messages.get('password'))

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'用户名或密码错误')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'用户已被锁定，请联系管理员解锁')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(forms.ModelForm):
    username = forms.RegexField(min_length=4, max_length=16, regex=r'^[a-zA-Z][a-zA-Z0-9_]*$', error_messages=error_messages.get('username'))
    email = forms.EmailField(min_length=6, max_length=32, error_messages=error_messages.get('email'))
    password = forms.CharField(min_length=6, max_length=16,error_messages=error_messages.get('password'))
    res_password = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        self.user = None
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            UserProfile.objects.get(username=username)
            raise forms.ValidationError(u'该用户名已被使用')
        except UserProfile.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserProfile.objects.get(email=email)
            raise forms.ValidationError(u'该邮箱已被注册')
        except UserProfile.DoesNotExist:
            return email

    def clean_res_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('res_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'两次输入密码不一致')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(min_length=6, max_length=16, error_messages=error_messages.get('password'))
    password = forms.CharField(min_length=6, max_length=16, error_messages=error_messages.get('password'))
    res_password = forms.CharField(required=False)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        res_password = self.cleaned_data.get("respassword")
        if password and res_password and password != res_password:
            raise forms.ValidationError("两次密码不相同")
        return password



class ChangeUserImageForm(forms.Form):
    image = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(ChangeUserImageForm, self).__init__(*args, **kwargs)



