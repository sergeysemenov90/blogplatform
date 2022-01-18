from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, CommentCreateView, UserDetailView, \
    UserUpdateView, TagDetailView, BlogDetailView, BlogCreateView, PostDeleteView
from .services import like_or_dislike_post, user_follow_unfollow, add_or_remove_subscriber

urlpatterns = [
    path('posts', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete  ', PostDeleteView.as_view(), name='post_delete'),
    path('post/post_create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/like', like_or_dislike_post, name='post_like_or_dislike'),
    path('post/<int:pk>/leave_comment', CommentCreateView.as_view(), name='post_leave_comment'),
    path('@<pk>/', UserDetailView.as_view(), name='user_profile'),
    path('@<pk>/user_update', UserUpdateView.as_view(), name='user_update'),
    path('@<pk>/follow', user_follow_unfollow, name='user_follow_unfollow'),
    path('tags/<int:pk>', TagDetailView.as_view(), name='tag_detail'),
    path('<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_create', BlogCreateView.as_view(), name='blog_create'),
    path('@<pk>/subscribe', add_or_remove_subscriber, name='user_subscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)