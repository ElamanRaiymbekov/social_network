from django.db import models
from django.conf import settings
from comments.models import AbstractComment
from users.models import User

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Post(models.Model):
    text = models.TextField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'id {self.id}'

    def comments_count(self):
        return self.comments


class Comment(AbstractComment, MPTTModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return "{} - {}".format(self.user, self.post)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


class Rating(models.Model):

    RATE_CHOICES = (
        (1, 'Плохо'),
        (2, 'Не плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Супер!')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='rate', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
