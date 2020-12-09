from django.contrib import admin

# Register your models here.
from headLine.models import Article, UserProfile, Category, Comment

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Comment)
