from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    """Базовый класс пользователя сайта"""
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='media/user_image/%Y/%m/%d', blank=True, null=True)
    subscribers = models.ManyToManyField(to='self')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_profile', args=[str(self.pk)])


class Blog(models.Model):
    """Блог, посвященный определенной теме"""
    owner = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='blogs')
    name = models.CharField(max_length=200)
    description = models.TextField()
    followers = models.ManyToManyField(to=SiteUser)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тэг, определяющий тему записи"""
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Post(models.Model):
    """Класс записи в блоге пользователя"""
    author = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    blog = models.ForeignKey(to=Blog, on_delete=models.SET_NULL, related_name='posts', blank=True, null=True)
    tags = models.ManyToManyField(to=Tag, related_name='posts', blank=True)
    image = models.ImageField(upload_to='media/content_image/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(to=SiteUser, related_name='post_likes')
    time_to_read = models.PositiveIntegerField()
    source = models.CharField(max_length=250, blank=True, null=True)
    views_number = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created_at']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Комментарии к записям в блоге"""

    author = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class UserFollowing(models.Model):
    """Пользователи, на которых подписан юзер, и его подписчики"""

    followee = models.ForeignKey(to=SiteUser, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(to=SiteUser, related_name='followerss', on_delete=models.CASCADE)