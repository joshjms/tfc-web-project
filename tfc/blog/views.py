from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Post, Comment, Announcement
from .forms import PostForm, CommentForm

import random
import requests
from datetime import datetime, date

def index(request):
    latest_posts = Post.objects.filter()[:5]
    announcements = Announcement.objects.all()
    return render(request, 'blog/index.html', {
        'latest_posts' : latest_posts,
        'announcements' : announcements,
    })

def nav(request):
    return render(request, 'blog/nav.html')

# Authentication

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blog/login.html', {"message": "Incorrect username or password."})
    else:
        return render(request, 'blog/login.html', {})

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'blog/register.html', {"message": "Your password didn't match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'blog/register.html', {"message": "The username has already been taken."})

        newUser = User.objects.create_user(username, email, password)
        newUser.save()

        return HttpResponseRedirect(reverse('blog:index'))
    else:
        return render(request, 'blog/register.html', {})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

# Blog Methods

def view_blog(request, blog_id):
    post = get_object_or_404(Post, id = blog_id)
    if request.method == "POST":
        content = request.POST['content']
        author = request.user
        comment = Comment(author = author, content = content, post = post)
        comment.save()
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    comments = Comment.objects.all().filter(post = post)
    form = CommentForm
    return render(request, 'blog/view.html', {
        'post' : post,
        'comments' : comments,
        'form' : form,
    })

def list_blog(request):
    all_posts = Post.objects.all()
    return render(request, 'blog/list.html', {
        'all_posts' : all_posts,
    })

def create_blog(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:index'))
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        created_on = datetime.now()
        updated_on = datetime.now()
        author = request.user
        post = Post(title = title, author = author, updated_on = updated_on, created_on = created_on, content = content)
        post.save()
        return HttpResponseRedirect(reverse('blog:index'))
    form = PostForm()
    return render(request, 'blog/create.html', {'form' : form})

def edit_blog(request, blog_id):
    post = get_object_or_404(Post, id = blog_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    if post.author != request.user:
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.updated_on = datetime.now()
        post.save()
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    form = PostForm(instance = post)
    return render(request, 'blog/edit.html', {'form' : form})

def delete_blog(request, blog_id):
    post = get_object_or_404(Post, id = blog_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    if post.author != request.user:
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    post.delete()
    return HttpResponseRedirect(reverse('blog:index'))

def add_comment(request, blog_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:view', args = [blog_id]))
    