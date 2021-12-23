from django.shortcuts import render
from django.views.generic import ListView
from blog.models import Post


class InterestingPosts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'base.html'
