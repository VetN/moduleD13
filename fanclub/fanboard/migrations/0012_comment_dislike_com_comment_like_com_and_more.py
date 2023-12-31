# Generated by Django 4.2.1 on 2023-09-03 06:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fanboard', '0011_post_dislike_post_post_like_post_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislike_com',
            field=models.ManyToManyField(blank=True, related_name='dislike_com', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='like_com',
            field=models.ManyToManyField(blank=True, related_name='like_com', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('DR', 'Торговцы'), ('Tn', 'Танки'), ('LW', 'Кожевники'), ('Hl', 'Хилы'), ('PM', 'Зельевары'), ('QG', 'Квестгиверы'), ('DD', 'ДД'), ('SM', 'Мастера заклинаний'), ('BS', 'Кузнецы'), ('GM', 'Гилдмастеры')], max_length=64, verbose_name='категория'),
        ),
    ]
