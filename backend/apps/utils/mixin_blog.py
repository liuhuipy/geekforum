# -*- coding:utf-8 -*-

from blog.models import Article, Category, Link
from comments.models import Comment
from users.models import UserProfile


class BaseMixin:
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