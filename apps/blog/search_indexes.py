__author__ = 'liuhui'


import datetime
from haystack import indexes
from blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    category = indexes.DateTimeField(model_attr='category')
    create_time = indexes.DateTimeField(model_attr='create_time')


    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(create_time__in=datetime.datetime.now)
