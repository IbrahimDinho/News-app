from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from headLine.models import Article, Category, Comment
from headLine.api.api_serlializers import ArticleSerializer, CategorySerializer, CommentSerializer, UserSerializer


@api_view(['GET', 'POST'])
def article_view_all(request):
    if request.method == 'POST':
        print("POST on the article viewAll URL")
        article_serializer = ArticleSerializer(data=request.data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_201_CREATED)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        print("GET on the article viewAll URL")
        articles = Article.objects.all()
        article_serializer = ArticleSerializer(articles, many=True)
        return Response(article_serializer.data, status=status.HTTP_200_OK)
    else:
        print("Unsupported " + request.method + "on the article viewAll URL")
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def article_view_single(request, id):
    try:
        article = Article.objects.get(id=id)

    except Article.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET on the article viewSingle URL")
        article_serializer = ArticleSerializer(article, many=(id is None))
        return Response(article_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        print("PUT on the article viewSingle URL")
        article_serializer = ArticleSerializer(data=request.data)
        if article_serializer.is_valid():
            article = Article.objects.get(id=id)
            article_serializer.update(article, article_serializer.validated_data)
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print("DELETE on the article viewSingle URL")
        article.delete()
        return Response('Deleted', status=status.HTTP_200_OK)
    else:
        print("Unsupported " + request.method + "on the article viewSingle URL")
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def category_view_all(request):
    if request.method == 'POST':
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        categorys = Category.objects.all()
        category_serializer = CategorySerializer(categorys, many=True)
        return Response(category_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def category_view_single(request, id):
    try:
        category = Category.objects.get(id=id)

    except Category.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        category_serializer = CategorySerializer(category, many=(id is None))
        return Response(category_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category = Category.objects.get(id=id)
            category_serializer.update(category, category_serializer.validated_data)
            return Response(category_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response('Deleted', status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def comment_view_all(request):
    if request.method == 'POST':
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        comments = Comment.objects.all()
        comment_serializer = CommentSerializer(comments, many=True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_view_single(request, id):
    try:
        comment = Comment.objects.get(id=id)

    except Comment.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comment_serializer = CommentSerializer(comment, many=(id is None))
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment = Comment.objects.get(id=id)
            comment_serializer.update(comment, comment_serializer.validated_data)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response('Deleted', status=status.HTTP_200_OK)


@api_view(['GET'])
def user_view_single(request, id):
    try:
        user = User.objects.get(id=id)

    except User.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user, many=(id is None))
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def user_view_all(request):
    
    if request.method == 'GET':
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)