from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import PIL

from blog.models import Article
from users.models import UserProfile
from djangoblog import settings


from .forms import LoginForm, RegisterForm, ResetPasswordForm, ForgetPasswordForm

# Create your views here.

@csrf_protect
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user is not None:
                auth_login(request, user)
                return HttpResponsePermanentRedirect(reverse('index-view'))
        else:
            auth_logout(request)
            print(login_form.errors)
            return render(request, 'users/login.html', {'errors': login_form.errors})

    else:
        login_form = LoginForm()
        user = None
    return render(request, 'users/login.html')

@csrf_protect
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index-view"))

@csrf_protect
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user is not None:
                success_title = u'恭喜您！liuhui开发者博客(liuhuiit.com)注册成功'
                return render(request, 'users/register_success.html', {'success_title': success_title})
        else:
            auth_logout(request)
            return render(request, 'users/register.html', {'errors': register_form.errors})
    else:
        register_form = RegisterForm()
        user = None
    return render(request, 'users/register.html')


@csrf_protect
@login_required
def reset_password(request):
    if request.method == 'POST':
        reset_form = ResetPasswordForm(request.POST)
        if reset_form.is_valid():
            user = reset_form.save()
            if user is not None:
                messages.success(request, '新密码设置成功！请重新登录')
                logout(request)
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.error(request, '当前密码输入错误')
                return render(request, 'users/reset_password.html', {'errors': reset_form.errors})
    else:
        reset_form = ResetPasswordForm(request)
        user = None
    return render(request, 'users/reset_password.html')


