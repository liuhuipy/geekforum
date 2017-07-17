__author__ = 'liuhui'


from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^search/', views.search, name='search'),
]


