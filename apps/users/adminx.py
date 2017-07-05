__author__ = 'liuhui'

import xadmin
from xadmin import views

from .models import Banner, Follower, EmailVerified


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "博客后台管理"
    site_footer = "开发者在线"
    menu_style = 'accordion'


class FollowerAdmin(object):
    list_display = ['user_a', 'user_b', 'create_time']
    search_fields = ['user_a', 'user_b']
    list_filter = ['user_a__username', 'user_b__username', 'create_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'rank', 'create_time']
    search_fields = ['title', 'image', 'url', 'rank']
    list_filter = ['title', 'image', 'url', 'rank', 'create_time']


class EmailVerifiedAdmin(object):
    list_display = ['user', 'token', 'timestamp']
    search_fields = ['user', 'token']
    list_filter = ['user__username', 'token', 'timestamp']


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Follower, FollowerAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(EmailVerified, EmailVerifiedAdmin)


