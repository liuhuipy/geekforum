#coding:utf8

__author__ = 'liuhui'

import xadmin
from xadmin import views

from .models import Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "博客后台管理"
    site_footer = "开发者在线"
    menu_style = 'accordion'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'rank', 'create_time']
    search_fields = ['title', 'image', 'url', 'rank']
    list_filter = ['title', 'image', 'url', 'rank', 'create_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Banner, BannerAdmin)

