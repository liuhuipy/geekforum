#coding:utf8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from blog.models import Article, Category, Link
from comments.models import Comment
from users.models import UserProfile
from djangoblog import settings
from django.core.cache import caches
from django.contrib import messages
from django.core.urlresolvers import reverse

from blog.forms import UEditorForm

cache = caches['default']

# Create your views here.

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()[:10]
        context['hot_article_list'] = Article.objects.order_by("-reading_num")[:10]
        context['new_comment_list'] = Comment.objects.order_by("-create_time")[:5]
        context['hot_user_list'] = UserProfile.objects.order_by("au")[:8]
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
        article_id = self.kwargs.get('article_id', '')
        kwargs['comment_list'] = Comment.objects.filter(article_id=article_id).all()
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

def ArticleEdit(request):
    if request.method == "POST":
        ueditorform = UEditorForm(request.POST)
        user = request.user
        if ueditorform.is_valid():
            article = Article.objects.create(author_id=user.pk,
                                             category_id=ueditorform.clean()['category'],
                                             title=ueditorform.clean()['title'],
                                             article_from=ueditorform.clean()['article_from'],
                                             summary=ueditorform.clean()['summary'],
                                             tags=ueditorform.clean()['tags'],
                                             content=ueditorform.clean()['content'],
                                             )
            if article is not None:
                user.topic_num += 1
                user.save()
                messages.success(request, '新密码设置成功！请重新登录')
                return HttpResponseRedirect(reverse('index-view'))
    else:
        ueditorform = UEditorForm()
    return render(request,'blog/article_edit.html',{'form': ueditorform})
