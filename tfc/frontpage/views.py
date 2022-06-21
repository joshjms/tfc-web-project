from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate

def index(request):
    return render(request, 'frontpage/index.html', {})

def discord(request):
    return render(request, 'frontpage/discord.html', {})