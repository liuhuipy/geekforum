from django.shortcuts import render, render_to_response
from django.db.models import Q
from blog.models import Article, Category, Link
from comments.models import Comment
from users.models import UserProfile

# Create your views here.


def search(request):
    q = request.GET['q']
    article_list = Article.objects.filter(Q(title__icontains=q) | Q(category__name__icontains=q) | Q(tags__icontains=q))
    category_list = Category.objects.all()[:10]
    hot_article_list = Article.objects.order_by("-reading_num")[:10]
    new_comment_list = Comment.objects.order_by("-create_time")[:5]
    hot_user_list = UserProfile.objects.order_by("au")[:8]
    link_list = Link.objects.order_by('-create_time')
    colors = ['primary', 'success', 'info', 'warning', 'danger']
    for index, link in enumerate(link_list):
        link.color = colors[index % len(colors)]
    return render(request, 'blog/index.html',{'article_list': article_list,
                                              'category_list': category_list,
                                              'hot_article_list': hot_article_list,
                                              'new_comment_list': new_comment_list,
                                              'hot_user_list': hot_user_list,
                                              'link_list': link_list,})