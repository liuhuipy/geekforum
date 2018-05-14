#coding:utf8
__author__ = 'liuhui'

from django import forms
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.forms import UEditorField
from blog.models import Article, Category

class UEditorForm(forms.Form):

    try:
        CATEGORY = Category.objects.all().values_list('id', 'name')
    except Category.DoesNotExist as e:
        print(e)
    else:
        CATEGORY = [
            (0,'python'),
            (1,u'前端'),
        ]
    ARTICLE_FROM = [
        (0, u'原创'),
        (1, u'转载'),
    ]
    title = forms.CharField(label=u'标题',widget=forms.TextInput(attrs={'class': 'form-control', 'name':'title','placeholder':u'请输入文章标题'}))
    category = forms.IntegerField(label=u'类型',widget=forms.Select(choices=CATEGORY,attrs={'class':'form-control'}))
    article_from = forms.IntegerField(label=u'来源',widget=forms.Select(choices=ARTICLE_FROM,attrs={'class':'form-control'}))
    summary = forms.CharField(label=u'摘要',widget=forms.Textarea(attrs={'class': 'form-control','placeholder':u'请输入文章摘要'}))
    tags = forms.CharField(label=u'标签',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':u'请输入文章标签，用逗号分隔，最多输入三个标签'}))
    content = UEditorField(label=u'正文', width=810, height=500, imagePath='article/ueditor/',filePath='article/ueditor/',toolbars='full')

    def __init__(self, *args, **kwargs):
        super(UEditorForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.choices = Category.objects.all().values_list('id','name')

    def clean(self):
        title = self.cleaned_data.get('title')
        article_from = self.cleaned_data.get('article_from')
        category = self.cleaned_data.get('category')
        summary = self.cleaned_data.get('summary')
        tags = self.cleaned_data.get('tags')
        content = self.cleaned_data.get('content')
        return self.cleaned_data

