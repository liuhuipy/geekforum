__author__ = 'liuhui'


from django.conf.urls import url, include

from users.views import LoginView
from users import views

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]