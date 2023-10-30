# Generated by Django 4.2.1 on 2023-10-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fanboard', '0015_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('LW', 'Кожевники'), ('PM', 'Зельевары'), ('Hl', 'Хилы'), ('Tn', 'Танки'), ('QG', 'Квестгиверы'), ('DD', 'ДД'), ('BS', 'Кузнецы'), ('SM', 'Мастера заклинаний'), ('GM', 'Гилдмастеры'), ('DR', 'Торговцы')], max_length=64, verbose_name='категория'),
        ),
    ]