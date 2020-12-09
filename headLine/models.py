from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, default=None)
    profile_photo = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User, dispatch_uid='new_user_profile_rcv')
def save_or_update_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        print('Creating Profile')
        profile = UserProfile(user=user)
        profile.save()


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)
    category_description = models.TextField()
    selected_by = models.ManyToManyField(User, related_name='category_selections', blank=True)

    def __str__(self):
        return self.category_name


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=200)
    article_summary = models.TextField()
    article_body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article')
    liked_by = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField()
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='child_comments')

    def __str__(self):
        return "Comment " + str(self.id) + "  article " + self.article.article_title
