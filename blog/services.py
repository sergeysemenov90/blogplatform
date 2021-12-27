from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from blogplatform import settings
from blog.models import Post, UserFollowing, SiteUser
from blog.tasks import send_mail_for_subscribers
from django.db.models.signals import pre_save, post_save


def like_or_dislike_post(request, pk):
    """Ставит лайк записи, если пользователь этого не делал ранее, иначе - убирает лайк"""
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse_lazy('post_detail', kwargs=({'pk': post.pk})))


def user_follow_unfollow(request, pk):
    """Подписка/отписка от пользователя, по аналогии с лайками"""
    user_follower = get_object_or_404(SiteUser, id=request.user.id)
    user_to_follow = get_object_or_404(SiteUser, id=request.POST.get('user_id'))
    follow = user_to_follow.followerss.filter(followee=user_follower)
    if follow.exists():
        follow.delete()
    else:
        UserFollowing.objects.create(followee=user_follower, follower=user_to_follow)
    return HttpResponseRedirect(reverse_lazy('user_profile', kwargs=({'pk': user_to_follow.pk})))


@receiver(pre_save, sender=Post)
def time_to_read(sender, instance, *args, **kwargs):
    """Заполняет значение time_to_read - время на чтения записи"""
    symbols_count = len(instance.content)
    res = int(symbols_count/1200)
    if res < 1:
        instance.time_to_read = 1
    else:
        instance.time_to_read = res


@receiver(post_save, sender=Post)
def send_mail_to_subscribers(sender, instance, *args, **kwargs):
    """Отправляет письмо с содержанием записи списку подписчиков"""
    if instance.author.subscribers:
        content = dict()
        content['emails'] = [subscriber.email for subscriber in instance.author.subscribers.all()]
        content['author'] = instance.author.get_full_name()
        content['post'] = instance.get_absolute_url()
        send_mail_for_subscribers.delay(content)
        print(content)
        print(list(content['emails']))



def add_or_remove_subscriber(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = get_object_or_404(SiteUser, pk=pk)
    subscriber = get_object_or_404(SiteUser, pk=request.user.id)
    subscribe = user.subscribers.filter(id=subscriber.id)
    if subscribe.exists():
        user.subscribers.remove(subscriber)
    else:
        user.subscribers.add(subscriber)
    return HttpResponseRedirect(reverse_lazy('user_profile', kwargs={'pk': user.id}))