from django.db import models
from django.contrib.auth.models import AbstractUser

class SiteUser(AbstractUser):
    """Базовый класс пользователя сайта"""
    image = models.ImageField(upload_to='media/user_image/%Y/%m/%d', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Post(models.Model):
    """Класс записи в блоге пользователя"""
    author = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/content_image/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(blank=True, null=True)
    claps = models.IntegerField(default=0)
    time_to_read = models.TimeField(blank=True, null=True) # TODO: написать функцию для подсчета времени на чтение

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.pk)])


class Comment(models.Model):
    author = models.ForeignKey(to=SiteUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'




