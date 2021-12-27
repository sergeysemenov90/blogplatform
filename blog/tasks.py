from django.core.mail import send_mail
from .models import SiteUser
from blogplatform.celery import app


@app.task
def send_mail_for_subscribers(content: dict):
    """Рассылает письма по емейлам, указанным в переданном словаре"""
    send_mail(
        f'Новая публикация от {content["author"]}!',
        f'Вы можете прочесть его полностью по ссылке  127.0.0.1:8000{content["post"]}',
        'Blogplatform',
        content['emails'],
        fail_silently=False
    )



@app.task
def send_beat_email():
    for user in SiteUser.objects.all():
        send_mail('Здравствуйте! Это наша прекрасная рассылка',
                  'Высылаем список самых интересных постов за эту неделю',
                  'semenovsg90@gmail.com',
                  [user.email,],
                  fail_silently=False
                  )