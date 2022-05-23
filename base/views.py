from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = 'context message here'
    return render(request, 'base/home.html', {'context': context})

def room(request):
    return HttpResponse('room')

