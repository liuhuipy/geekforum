#coding:utf8
from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import UserProfile

from .forms import LoginForm, RegisterForm, ChangeUserImageForm, PasswordChangeForm

# Create your views here.

@csrf_protect
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user is not None:
                auth_login(request, user)
                return HttpResponsePermanentRedirect(request.session['LoginForm'])
        else:
            auth_logout(request)
            print(login_form.errors)
            return render(request, 'users/login.html', {'errors': login_form.errors})

    else:
        login_form = LoginForm()
        user = None
        request.session['LoginForm'] = request.META.get('HTTP_REFERER', '/')
    return render(request, 'users/login.html')

@csrf_protect
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@csrf_protect
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user is not None:
                user = authenticate(username=register_form.cleaned_data['username'],password=register_form.cleaned_data['password'])
                auth_login(request,user)
                return HttpResponseRedirect(reverse('index-view'))
        else:
            auth_logout(request)
            return render(request, 'users/register.html', {'errors': register_form.errors})
    else:
        register_form = RegisterForm()
        user = None
    return render(request, 'users/register.html')


@csrf_protect
@login_required
def password(request):
    user = request.user

    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            data = form.clean()
            if user.check_password(data["old_password"]):
                user.set_password(data["password"])
                user.save()
                messages.success(request, "新密码设置成功！请重新登录")
                auth_logout(request)
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.error(request,'当前密码输入错误')
                return render(request, "users/password.html", {'errors': form.errors})
    else:
        form = PasswordChangeForm()

    return render(request, "users/password.html")

def updateImage(request):
    if request.method == 'POST':
        form = ChangeUserImageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            user = request.user
            user.image = image
            user.save()
            return HttpResponseRedirect(reverse('index-view'))
    else:
        form = ChangeUserImageForm()
    return render(request, 'users/changeuserimage.html',{'form':form})


