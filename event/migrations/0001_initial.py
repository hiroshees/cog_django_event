# Generated by Django 4.2.7 on 2023-12-13 05:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='新規登録日時')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('number', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='定員')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='新規登録日時')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.category', verbose_name='カテゴリ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='主催者')),
            ],
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='新規登録日時')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event', verbose_name='イベント')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=100, verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='新規登録日時')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event', verbose_name='イベント')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
    ]
