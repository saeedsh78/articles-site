from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from django.db.models import Q
from account.models import User
from .models import Article, Category
from django.core.paginator import Paginator


# Create your views here.
def home(request, page=1):
    articles_list = Article.objects.published()
    paginator = Paginator(articles_list, 5)
    articles = paginator.get_page(page)
    context = {
        'articles': articles
    }
    return render(request, 'blog/index.html', context)


def detail_article(request, slug):
    article =  get_object_or_404(Article.objects.published(), slug=slug, status='p')
    ip_address = request.user.ip_address

    if ip_address not in article.hits.all():
        article.hits.add(ip_address)

    context = {
        'article': article
    }
    return render(request, 'blog/article.html', context)


def preview_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user and article.status in ['d', 'b'] or request.user.is_superuser:
        context = {
            'article': article
        }
    else:
        raise Http404("You can't see this page.")
    return render(request, 'blog/article.html', context)


def category(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug, status=True)
    articles_list = category.articles.published()
    paginator = Paginator(articles_list, 5)
    articles = paginator.get_page(page)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blog/category_list.html', context)


def author_article(request, username, page=1):
    author = get_object_or_404(User, username=username)
    articles_list = author.articles.published()
    paginator = Paginator(articles_list, 5)
    articles = paginator.get_page(page)
    context = {
        'author': author,
        'articles': articles
    }
    return render(request, 'blog/author_list.html', context)


def search_list(request, page=1):
    search = request.GET.get('q')
    articles_list = Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))
    paginator = Paginator(articles_list, 5)
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'search': search
    }
    return render(request, 'blog/search_list.html', context)
