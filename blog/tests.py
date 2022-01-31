import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post, SiteUser


def create_user():
    user = SiteUser.objects.create(first_name='Alexey', last_name='Popov')
    return user


def create_post(days,
                user,
                title='First_post',
                content='First_post_content',
                image='a',
                ):
    time = timezone.now() + datetime.timedelta(days)
    post = Post.objects.create(author=user, title=title, content=content, image=image)
    post.created_at = time
    post.save()
    return post


class PostListViewTest(TestCase):
    def test_no_posts(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кажется вы ни на кого не подписаны...')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_future_posts(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        user = create_user()
        post = create_post(user=user, days=30)
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Кажется вы ни на кого не подписаны...')
        self.assertQuerysetEqual(response.context['posts'], [])

