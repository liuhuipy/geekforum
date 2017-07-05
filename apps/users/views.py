from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone

from .forms import LoginForm
from .models import UserProfile

import datetime
import re
import json
import random

# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')
    def post(self, request):
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return HttpResponsePermanentRedirect(reverse('index-view'))
                return render(request, 'users/login.html', {'msg': '用户名或密码错误'})
            return render(request, 'users/login.html', {'form_errors': login_form.errors})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index-view"))
