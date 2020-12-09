from django.urls import path
from .api_views import article_view_all, article_view_single, category_view_single, category_view_all, \
    comment_view_single, comment_view_all, user_view_all, user_view_single

urlpatterns = [
    path('articles/', article_view_all, name="article_view_all"),
    path('articles/<int:id>', article_view_single, name="article_view_single"),
    path('categories/', category_view_all, name="category_view_all"),
    path('categories/<int:id>', category_view_single, name="category_view_single"),
    path('comments/', comment_view_all, name="comment_view_all"),
    path('comments/<int:id>', comment_view_single, name="comment_view_single"),
    path('users/', user_view_all, name="user_view_all"),
    path('users/<int:id>', user_view_single, name="user_view_single"),

]
