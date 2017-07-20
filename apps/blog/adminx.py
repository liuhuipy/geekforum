__author__ = 'liuhui'

import xadmin

from .models import Article, Category, Link


class ArticleAdmin(object):
    list_display = ['author', 'category', 'tags', 'title', 'article_from', 'reading_num', 'is_top', 'rank', 'status', 'create_time', 'update_time']
    search_fields = ['author', 'category', 'tags', 'title', 'summary', 'article_from', 'content', 'reading_num', 'is_top', 'rank', 'status']
    list_filter = ['author__username', 'category__name', 'tags', 'summary', 'article_from', 'content', 'reading_num', 'is_top', 'rank', 'status', 'create_time', 'update_time']
    readonly_fields = []
    style_fields = {'content': 'ueditor'}
    relfield_style = 'fk-ajax'

class CategoryAdmin(object):
    list_display = ['name', 'rank', 'create_time', 'update_time']
    search_fields = ['name', 'rank']
    list_filter = ['name', 'rank', 'create_time', 'update_time']


class LinkAdmin(object):
    list_display = ['name', 'url', 'rank', 'create_time', 'update_time']
    search_fields = ['name', 'url', 'rank']
    list_filter = ['name', 'url', 'rank', 'create_time', 'update_time']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Link, LinkAdmin)




