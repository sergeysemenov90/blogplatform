import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, SiteUser, UserFollowing, Tag, Blog
from .forms import CommentCreateForm, PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    """Отображения списка постов пользователей"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Реализация поиска по заголовкам записей"""
        queryset = Post.objects.all()
        if 'search' in self.request.GET:
            queryset = queryset.filter(title__icontains=self.request.GET['search'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(PostListView, self).get_context_data()
        if self.request.user.is_authenticated:
            follow_to = UserFollowing.objects.filter(followee=self.request.user.id)
            follow_list = [userfollowerobject.follower for userfollowerobject in follow_to]
            print(follow_list)
            data['interesting_posts'] = Post.objects.filter(author__in=follow_list)
        return data


class PostDetailView(DetailView):
    """Детальное отображение конкретной записи"""
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """Переопределяем метод для добавления в шаблон данных о наличии лайка от пользователя"""
        data = super(PostDetailView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        is_liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        data['likes_count'] = post.likes.count()
        data['is_liked'] = is_liked
        data['form'] = CommentCreateForm()
        return data


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание записи"""
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        """Переопределяем метод для добавления автора записи"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs=({'pk': self.object.pk}))


class PostUpdateView(UpdateView):
    """Редактирование записи"""
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_update.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        form.instance.edited_at = datetime.datetime.now()
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    """Удаление публикации пользователя"""
    model = Post
    template_name = 'blog/post_delete.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('user_profile', args=[str(user.pk)])


class UserUpdateView(UpdateView):
    """Обновление данных пользователя"""
    model = SiteUser
    fields = ['first_name', 'last_name', 'email', 'description', 'image']
    template_name = 'blog/user_update.html'

    def get_success_url(self):
        return reverse_lazy('user_profile', args=(self.kwargs['pk'],))


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария"""
    model = Comment
    form_class = CommentCreateForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        """Переопределяем метод для добавления автора и записи для комментария"""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs=({'pk': self.object.post.pk}))


class UserDetailView(DetailView):
    """Страница пользователя"""
    model = SiteUser
    template_name = 'blog/user_profile.html'
    context_object_name = 'siteuser'

    def get_context_data(self, **kwargs):
        user = get_object_or_404(SiteUser, id=self.kwargs['pk'])
        context = super().get_context_data()
        context['following'] = UserFollowing.objects.filter(follower=user)
        context['followers'] = UserFollowing.objects.filter(followee=user)
        is_follow = False
        is_subscribed = False
        if self.request.user.is_authenticated:
            follow = user.followerss.filter(followee=self.request.user)
            if follow.exists():
                is_follow = True
            subscribe = user.subscribers.filter(id=self.request.user.id)
            if subscribe.exists():
                is_subscribed = True
        context['is_follow'] = is_follow
        context['is_subscribed'] = is_subscribed
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.pk})




# TODO: Ajax для отправки post без перезагрузки страницы
# TODO Количество просмотров поста
