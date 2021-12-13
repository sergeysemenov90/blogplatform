from django.contrib import admin

from .models import SiteUser, Post, Comment


admin.site.register((SiteUser, Post, Comment),)