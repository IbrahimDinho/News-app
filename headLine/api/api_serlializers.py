from django.contrib.auth.models import User
from rest_framework import serializers

from headLine.models import Article, Category, UserProfile, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('article_title', 'article_body', 'category', 'id', 'liked_by', 'comments', 'article_summary')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_description', 'selected_by')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'article', 'user', 'body', 'parent_comment', 'child_comments')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model = User
       fields = ('username', 'email', 'first_name', 'last_name')