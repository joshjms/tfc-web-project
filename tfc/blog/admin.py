from django.contrib import admin
from blog.models import Post, Comment, Announcement

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Announcement)