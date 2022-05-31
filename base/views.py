from turtle import pos
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .classes.table_joins import Post_user
from django.db.models import Q

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = user)
        except:
            print("Error - user / password incorrect, does not exist.")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("User does not exist.")

    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    posts = Post.objects.all()
    username = request.user.username
    user_id = request.user.id 
    
    if username is None or user_id is None:
        username = "NoUserName"
        user_id = 0

    context = {'posts': posts, 'username': username, 'user_id': user_id}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def myposts(request):
    user_id = request.user.id 
    username = request.user.username

    results_list = Post.objects.filter(user=user_id)
    context = {'user_id': user_id, 'username': username, 'posts': results_list}

    return render(request, 'base/myposts.html', context)


def commentspost(request, pk):
    post = Post.objects.filter(id=pk)
    comments = Comment.objects.filter(post_id=pk).values()
    users = User.objects.filter(comment__post_id=pk).only('id', 'username')
    
    context = {'posts': post, "comments": comments, 'users': users}
    return render(request, 'base/commentspost.html', context)

@login_required(login_url='login')
def createpost(request):
    if request.method == "POST":
        user_id = request.user.id 
        header, body = request.POST["header"], request.POST["body"]
        
        post_instance = Post.objects.create(header=header, body=body, user_id=user_id)
        post_instance.save()

        return redirect('myposts')
    else:
        return render(request, 'base/components/create_post_component.html')


@login_required(login_url='login')
def deletepost(request, pk):
    post = Post.objects.filter(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('myposts')
    
    context = {'posts': post}
    return render(request, 'base/deletepost.html', context)



"""

    #users = User.objects.values_list('username', flat=True).filter(Q(comment__user_id=1) & Q(comment__post_id=16))
    #usersORGINAL = User.objects.filter(Q(comment__post_id=pk))
    #users = User.objects.filter(comment__user_id=1).all()

    data = Comment.objects.filter(body='Defo Mafia!').values()
 

"""
