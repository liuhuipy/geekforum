from django.db import models

from .CustomUser import CustomUser
from .BaseModel import BaseModel


class ArticleTag(BaseModel):
    name = models.CharField(max_length=32, unique=True, verbose_name='文章标签')
    key = models.CharField(max_length=16, unique=True, verbose_name='标签key')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='创建人')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    title = models.CharField(max_length=64, verbose_name='文章标题')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='创建人')
    tags = models.ManyToManyField(ArticleTag, related_name='article_tags', verbose_name='标签')
    description = models.TextField(verbose_name='详情')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论文章')
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               related_name='parent_comment',
                               blank=True,
                               null=True,
                               verbose_name='父评论')
    content = models.TextField(verbose_name='评论内容')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article.title

