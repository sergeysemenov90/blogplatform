from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView
from .services import like_or_dislike_post

urlpatterns = [
    path('', PostListView.as_view(), name='mainpage'),
    path('posts', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/post_create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/like', like_or_dislike_post, name='post_like_or_dislike')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)