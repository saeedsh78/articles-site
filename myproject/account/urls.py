# The views used below are normally mapped in the AdminSite instance.
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from .views import ArticleList, ArticleCreate, ArticleUpdate, ArticleDelete, Profile, CategoryCreate

app_name = 'account'

urlpatterns = [
    path("", ArticleList.as_view(), name='home'),
    path("article/create", ArticleCreate.as_view(), name='article-create'),
    path("article/update/<int:pk>", ArticleUpdate.as_view(), name='article-update'),
    path("article/delete/<int:pk>", ArticleDelete.as_view(), name='article-delete'),
    path("profile/", Profile.as_view(), name='profile'),
    path('category/create', CategoryCreate.as_view(), name='category-create'),

]