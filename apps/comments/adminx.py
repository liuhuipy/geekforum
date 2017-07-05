__author__ = 'liuhui'

import xadmin

from .models import Comment


class CommentAdmin(object):
    list_display = ['user', 'article', 'text', 'create_time', 'parentcomment']
    search_fields = ['user', 'article', 'text', 'parentcomment']
    list_filter = ['user__username', 'article__title', 'text', 'create_time', 'parentcomment']
    field = ['user__username', 'article_title']

xadmin.site.register(Comment, CommentAdmin)
