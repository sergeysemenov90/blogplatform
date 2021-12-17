from django.contrib import admin

from .models import SiteUser, Post, Comment, Blog, Tag

admin.site.register((SiteUser, Post, Comment, Blog, Tag),)