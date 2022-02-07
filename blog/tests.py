import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from blog.models import Post, SiteUser


def create_user():
    user = SiteUser.objects.create(first_name='Alexey', last_name='Popov')
    return user


def create_post(user,
                days=0,
                title='First_post',
                content='First_post_content',
                image='a',
                personal=False,
                ):
    time = timezone.now() + datetime.timedelta(days)
    post = Post.objects.create(author=user, title=title, content=content, image=image, personal=personal)
    post.created_at = time
    post.save()
    return post


class PostListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

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
        post = create_post(user=self.user, days=30)
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Кажется вы ни на кого не подписаны...')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_posts_list(self):
        post = create_post(user=self.user, )
        response = self.client.get(reverse('post_list'))
        self.assertIn(post, response.context['posts'])

    def test_personal_post(self):
        post = create_post(user=self.user, personal=True)
        response = self.client.get(reverse('post_list'))
        self.assertNotIn(post, response.context['posts'])


class PostDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.first_post = create_post(user=self.user, )
        self.second_post = create_post(user=self.user, personal=True)
        self.response1 = self.client.get(reverse('post_detail', args=[self.first_post.id, ]))
        self.response2 = self.client.get(reverse('post_detail', args=[self.second_post.id, ]))

    def test_post_accessibility(self):
        self.assertEqual(self.response1.status_code, 200)
        self.assertContains(self.response1, self.first_post.title)

    def test_post_views_number(self):
        self.first_post.refresh_from_db()
        self.assertEqual(self.response1.context['post'], self.first_post)
        self.assertEqual(self.first_post.views_number, 1)

    def test_personal_post(self):
        self.assertEqual(self.response2.status_code, 403)
