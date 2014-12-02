# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from resume.core.models import Article, Tag
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
import markdown
from decouple import config
import twitter


def home(request):
    api = twitter.Api(consumer_key=config('consumer_key'),
                      consumer_secret=config('consumer_secret'),
                      access_token_key=config('access_token_key'),
                      access_token_secret=config('access_token_secret')
                     )
    statuses = api.GetUserTimeline(screen_name='AlexFalcucci')
    posts = [s.text for s in statuses]
    all_articles = Article.get_published()

    return render(request, 'core/index.html', {'posts':posts[0:10], 'articles':all_articles[0:10]})

def _articles(request, articles):
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'core/blog/all_articles.html', {
        'articles': articles,
        'popular_tags': popular_tags
    })

def all_articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)

def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    return render(request, 'core/blog/article.html', {'article': article})