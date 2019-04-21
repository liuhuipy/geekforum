# -*- coding:utf-8 -*-

from blog.models import Category
from .mixin_login import LoginRequiredMixin


class NavInfoMixin(LoginRequiredMixin):
    def get_context_data(self, *args, **kwargs):
        context = super(NavInfoMixin, self).get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()[:10]
        return context
