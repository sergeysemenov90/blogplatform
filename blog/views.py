from django.views.generic import ListView, DetailView
from .models import Post

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
