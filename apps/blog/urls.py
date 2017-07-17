__author__ = 'liuhui'

from django.conf.urls import url, include
from blog.views import IndexView, ArticleDetailView, CategoryView, TagView, ArticleEdit

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index-view"),
    url(r'^article/(?P<article_id>\d+)/$', ArticleDetailView.as_view(), name='article-view'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-view'),
    url(r'^tag/(?P<tag>\d+)/$', TagView.as_view(), name='tag-view'),
    url(r'article_edit/$', ArticleEdit, name='article-edit'),
]