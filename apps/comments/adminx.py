__author__ = 'liuhui'

import xadmin

from .models import Comment


class CommentAdmin(object):
    list_display = ['user', 'article', 'text', 'create_time', 'parent']
    search_fields = ['user', 'article', 'text', 'parent']
    list_filter = ['user__username', 'article__title', 'text', 'create_time', 'parent']
    #field = ['user__username', 'article_title']
    ordering = ['user', 'article']

xadmin.site.register(Comment, CommentAdmin)
