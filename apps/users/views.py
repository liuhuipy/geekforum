from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView

from blog.models import Article
from users.models import UserProfile
from djangoblog import settings


from .forms import LoginForm, RegisterForm, ResetPasswordForm, ForgetPasswordForm

# Create your views here.


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


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index-view"))


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

@login_required
def reset_password(request):
    if request.method == 'POST':
        reset_form = ResetPasswordForm(request)
        if reset_form.is_valid():
            user = request.user
            password = reset_form.cleaned_data.get('password')
            user.set_password(password)
            user.updated = timezone.now()
            user.save()
            return render(request, 'users/reset_password.html', {'success_message': u'您的账号密码修改成功！'})
        else:
            return render(request, 'users/reset_password.html', {'errors': reset_form.errors})
    else:
        reset_form = ResetPasswordForm(request)
        user = None
    return render(request, 'users/reset_password.html')


class UserView(DetailView):
    model = UserProfile
    template_name = 'users/userinfo.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'


    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        user_id = self.kwargs.get('user_id', '')
        kwargs['article_list'] = Article.objects.filter(author__id=user_id).order_by('-create_time')
        return super(UserView, self).get_context_data(**kwargs)
