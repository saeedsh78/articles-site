from django.urls import path, re_path
from .views import (home,
                    detail_article,
                    category,
                    author_article,
                    preview_article,
                    search_list,
                    )

app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),
    path('page/<int:page>', home, name='home'),
    path('article/<slug:slug>', detail_article, name='detail_article'),
    path('preview/<int:pk>', preview_article, name='preview_article'),
    path('category/<slug:slug>', category, name='category'),
    path('category/<slug:slug>/page/<int:page>', category, name='category'),
    path('author/<slug:username>', author_article, name='author'),
    path('author/<slug:username>/page/<int:page>', author_article, name='author'),
    path('search/', search_list, name='search'),
    path('search/page/<int:page>', search_list, name='search'),
]
