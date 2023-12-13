from django.db import models
from django.core import validators
from user.models import CustomUser


# Create your models here.
class Category(models.Model):
    name = models.CharField(
        verbose_name='名前',
        max_length=100
    )
    created_at = models.DateTimeField(
        verbose_name='新規登録日時',
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(
        verbose_name='名前',
        max_length=100
    )
    number = models.IntegerField(
        verbose_name = '定員',
        default=0,
        validators=[
            validators.MinValueValidator(0)
        ]
    )
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='主催者',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name='新規登録日時',
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )

    def __str__(self):
        return self.name


class EventUser(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name='イベント',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザ',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name='新規登録日時',
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )

    def __str__(self):
        return self.id


class Chat(models.Model):
    body = models.CharField(
        verbose_name='本文',
        max_length=100
    )
    event = models.ForeignKey(
        Event,
        verbose_name='イベント',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザ',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name='新規登録日時',
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )

    def __str__(self):
        return str(self.id)

