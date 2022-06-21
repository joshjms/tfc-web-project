from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.urls import reverse_lazy, reverse

# Create your models here.

class Post(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 200, unique = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    updated_on = models.DateTimeField(auto_now = True)
    created_on = models.DateTimeField(auto_now_add = True)
    content = RichTextField(blank = True, null = True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('index')

class Comment(models.Model):
    id = models.IntegerField(primary_key = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)
    content = RichTextField(blank = True, null = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('index')

class Announcement(models.Model):
    id = models.IntegerField(primary_key = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)
    content = RichTextField(blank = True, null = True)