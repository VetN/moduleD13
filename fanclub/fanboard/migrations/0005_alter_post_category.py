# Generated by Django 4.2.1 on 2023-08-15 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fanboard', '0004_post_file_post_video_profile_site_profile_vk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('GM', 'Гилдмастеры'), ('SM', 'Мастера заклинаний'), ('LW', 'Кожевники'), ('BS', 'Кузнецы'), ('Hl', 'Хилы'), ('QG', 'Квестгиверы'), ('DR', 'Торговцы'), ('Tn', 'Танки'), ('PM', 'Зельевары'), ('DD', 'ДД')], max_length=64, verbose_name='категория'),
        ),
    ]
