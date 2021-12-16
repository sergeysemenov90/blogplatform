from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Comment
from .forms import CommentCreateForm


class PostListView(ListView):
    """Отображения списка постов пользователей"""
    model = Post
    template_name = 'base.html'
    context_object_name = 'posts'


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


class PostCreateView(CreateView):
    """Создание записи"""
    model = Post
    fields = ['title', 'content', 'image', ]
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        """Переопределяем метод для добавления автора записи"""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """Редактирование записи"""
    model = Post
    fields = ['title', 'content', 'image', ]
    template_name = 'blog/post_update.html'
    success_url = reverse_lazy('post_list')


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        """Переопределяем метод для добавления комментария"""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = get_object_or_404(Post, id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=(self.kwargs['pk'],))