from django import template
from django.utils import timezone
from django.db.models import Count, Q, Max, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from ..models import Category, Article
from star_ratings.models import UserRating
from datetime import datetime, timedelta

register = template.Library()


@register.simple_tag
def title():
    return "وبلاگ جنگویی"


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def popular_articles():
    last_month = datetime.now(tz=timezone.utc) - timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(count=Count('hits', filter=Q(articlehit__created__gt=last_month))
                                                            ).order_by('-count', '-publish')[:5],
        "title": 'مقالات پر بازدید ماه'
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def hot_articles():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    return {
        "articles": Article.objects.published().annotate(count=Count('comments', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id))
                                                            ).order_by('-count', '-publish')[:5],
        "title": 'مقالات داغ ماه'
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_rate_articles():
    last_month = datetime.now(tz=timezone.utc) - timedelta(days=30)
    user_ratings_in_last_month = UserRating.objects.filter(created__gt=last_month)
    top_articles = user_ratings_in_last_month.values('rating__object_id').annotate(
        count_score=Count('score'),
        average_score=Avg('score'),
    ).order_by('-average_score', '-count_score')

    articles = []
    for stat in top_articles:
        rating_object_id = stat['rating__object_id']
        try:
            article = Article.objects.published().get(id=rating_object_id)
            articles.append(article)
        except Exception as e:
            continue

    return {
        "articles": articles[:5],
        "title": 'مقالات پر امتیاز ماه'
    }