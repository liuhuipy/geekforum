from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView, View, DetailView
from blog.models import Article, Category, Link
from comments.models import Comment
from users.models import UserProfile
from djangoblog import settings
from django.db.models import Q
from django.core.cache import caches
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

cache = caches['default']

# Create your views here.

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()[:10]
        context['hot_article_list'] = Article.objects.order_by("-reading_num")[:10]
        context['new_comment_list'] = Comment.objects.order_by("-create_time")[:5]
        context['hot_user_list'] = UserProfile.objects.order_by("-topic_num")[:5]
        context['link_list'] = Link.objects.order_by('-create_time')

        colors = ['primary', 'success', 'info', 'warning', 'danger']
        for index, link in enumerate(context['link_list']):
            link.color = colors[index % len(colors)]
        return context


class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        article_list = Article.objects.filter(status=0).order_by('-create_time')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('rank')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(BaseMixin, DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()

        #文章点击数 + 1
        obj.reading_num += 1
        obj.save()

        return obj

    def get_context_data(self, **kwargs):
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = "article_list"
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['category_id'], status=0).order_by('-create_time')
        return article_list

    def get_context_data(self, **kwargs):
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        article_list = Article.objects.only('tags').filter(tags__icontains=self.kwargs['tag'], status=0)
        return article_list

    def get_context_data(self, **kwargs):
        return super(TagView, self).get_context_data(**kwargs)


