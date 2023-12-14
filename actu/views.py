from django.shortcuts import render
from django.urls import path
from datetime import datetime

from .models import Article

# Create your views here.


def article(request):
    all_article = Article.objects.order_by("createArticle")
    context = {'all_article': all_article}
    
    return render(request, 'article.html', context)