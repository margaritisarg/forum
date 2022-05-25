from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'base/home.html', context)

def post(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'base/post.html', context)




