from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Comment, SiteUser, UserFollowing
from .forms import CommentCreateForm
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
    fields = ['title', 'content', 'image', ]
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        """Переопределяем метод для добавления автора записи"""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs=({'pk': self.object.pk}))


class PostUpdateView(UpdateView):
    """Редактирование записи"""
    model = Post
    fields = ['title', 'content', 'image', ]
    template_name = 'blog/post_update.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', args=(self.kwargs['pk'],))


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария"""
    model = Comment
    form_class = CommentCreateForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        """Переопределяем метод для добавления автора и записи для комментария"""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = get_object_or_404(Post, id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs=({'pk': self.object.pk}))


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
        follow = user.followerss.filter(followee=self.request.user)
        if follow.exists():
            is_follow = True
        context['is_follow'] = is_follow
        return context




# TODO: Страница пользователя
# TODO: Страница блога
# TODO: Страница тэга
# TODO: Облако тэгов на главной
# TODO: Ajax для отправки post без перезагрузки страницы
# TODO: Переделать главную