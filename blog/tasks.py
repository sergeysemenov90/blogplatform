from django.core.mail import send_mail
from .models import SiteUser
from blogplatform.celery import app


@app.task
def send_beat_email():
    for user in SiteUser.objects.all():
        send_mail('Здравствуйте! Это наша прекрасная рассылка',
                  'Высылаем список самых интересных постов за эту неделю',
                  'semenovsg90@gmail.com',
                  [user.email,],
                  fail_silently=False
                  )