from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from blog.models import Article

from haystack.forms import SearchForm

# Create your views here.


def search(request):
    q = request.GET['q']
    error_msg = ''
    if not q:
        error_msg = u'请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    article_list = Article.objects.filter(Q(title__icontains=q) | Q(category__name__icontains=q) | Q(tags__icontains=q))
    return render(request, 'blog/index.html',{'error_msg': error_msg,
                                              'article_list': article_list})