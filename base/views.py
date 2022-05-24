from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = 'context message here'
    return render(request, 'base/home.html', {'context': context})

def post(request):
    posts = [
        {'id': 1, 'user': 'Jordan - posted 3 hours ago', 'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'},
        {'id': 2, 'user': 'Jenny - posted 5 hours ago', 'text': 'Lorem ipsum, consectetur adipisicing elit.'},
        {'id': 3, 'user': 'Mario - posted 6 hours ago', 'text': 'Lorem ipsum, consectetur adipisicing elit. consectetur adipisicing.'},
    ]
    return render(request, 'base/post.html', {'posts': posts})

