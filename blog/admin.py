from django.contrib import admin

from .models import SiteUser, Post


admin.site.register(SiteUser)
admin.site.register(Post)