#coding:utf8
from django.db import models
from django.conf import settings
from blog.models import Article
from datetime import datetime
# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'用户')
    article = models.ForeignKey(Article,verbose_name=u'文章')
    text = models.TextField(verbose_name=u'评论')
    is_removed = models.BooleanField(default=False)
    parent = models.ForeignKey('self',default=None,blank=True,null=True,verbose_name=u'父评论')
    likes_count = models.PositiveIntegerField(default=0,verbose_name=u'点赞数')

    create_time = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name=u'修改时间', blank=True, null=True)

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.article.title