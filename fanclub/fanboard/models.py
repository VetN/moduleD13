from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name='геймер' )
    pro_photo = models.ImageField(upload_to='image_user/', blank=True, null=True,verbose_name=' фото геймера' )
    site = models.URLField(max_length=255,  blank=True, null=True, verbose_name='веб-сайт')
    vk = models.URLField(max_length=255,  blank=True,null=True, verbose_name='аккаунт VK')
    ratingUser = models.SmallIntegerField(default=0)

    
    def __str__(self):
        return self.user.username


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def update_rating(self):
         # set возвращ множ self(главная модель рейтинг) post(зависимая мод)set(множество) aggregate (подсчитыв sum)
        postRat = self.post_set.all().aggregate(postRat=Sum('rating'))['postRat'] or 0
        commentRat = self.user.comment_set.all().aggregate(commentRat=Sum('rating'))['commentRat'] or 0
        self.ratingUser = postRat + commentRat
        self.save()

class Post(models.Model):
    
    cat = {
        ('Tn', 'Танки'),
        ('Hl', 'Хилы'),
        ('DD', 'ДД'),
        ('DR', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('BS', 'Кузнецы'),
        ('LW', 'Кожевники'),
        ('PM', 'Зельевары'),
        ('SM', 'Мастера заклинаний')
    }

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='геймер')
    category =models.CharField(max_length=64, choices=cat, verbose_name='категория')

    dataCreation = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    dataUpdate = models.DateTimeField(auto_now=True, verbose_name="редактировано")
    
    title = models.CharField(max_length=128, verbose_name='название')
    content = models.TextField()
    photo = models.ImageField(upload_to = 'image_photo/', blank=True, null=True, verbose_name='фото' )
    video = models.FileField(upload_to='video/', blank=True, null=True, verbose_name='видео')
    file = models.FileField(upload_to='file/', blank=True, null=True, verbose_name='другое')
    
    rating = models.SmallIntegerField(default=0)
    
    like_post = models.ManyToManyField(User, blank=True, related_name='like_post')
    dislike_post = models.ManyToManyField(User, blank=True, related_name='dislike_post')
    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

        # функция возращает только часть контента
    def preview(self):
        return self.content[0:100] + '...'
    
    def __str__(self):
        return self.title


    # для кеша если в класса добавлен метод переопределения
    #def save(self, *args, **kwargs):
        #super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        #cache.delete(f'статья-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его







class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор комментария")
    content = models.TextField(verbose_name="текст комментария")
    dataCreation = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    rating = models.SmallIntegerField(default=0)
    approved_comment = models.BooleanField(default=False, verbose_name='Комментарий одобрен')
    like_com = models.ManyToManyField(User, blank=True, related_name='like_com')
    dislike_com = models.ManyToManyField(User, blank=True, related_name='dislike_com')



    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.commentUser.username 
    
    def approved_commit_add(self):
        if True:
            self.approved_commit = True
        else:
            self.approved_commit = False
        return self.instance
    
    # функция возращает только часть контента
    def preview(self):
        return self.content[0:100] + '...'