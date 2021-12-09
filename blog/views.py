from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    """ Класс для отображения постов пользователей"""
    model = Post
    template_name = 'base.html'
    context_object_name = 'posts'
