from django.views.generic import ListView
from blog.models import Post, Tag


class InterestingPosts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'base.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['tags'] = Tag.objects.all()
        return context
