from django.db import models
from django.contrib.auth.models import AbstractUser

class SiteUser(AbstractUser):
    """Базовый класс пользователя сайта"""
    image = models.ImageField(upload_to='media/user_image/%Y/%m/%d', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Blog(models.Model):
    """Блог, посвященный определенной теме"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    followers = models.ManyToManyField(to=SiteUser, null=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class Post(models.Model):
    """Класс записи в блоге пользователя"""
    author = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    blog = models.ForeignKey(to=Blog, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='media/content_image/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(to=SiteUser, related_name='post_like')
    time_to_read = models.TimeField(blank=True, null=True) # TODO: написать функцию для подсчета времени на чтение

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['created_at']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.pk)])


class Comment(models.Model):
    """Комментарии к записям в блоге"""

    author = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Tag(models.Model):
    """Тэг, определяющий тему записи"""
    name = models.CharField(max_length=200)
    posts = models.ManyToManyField(to=Post)


