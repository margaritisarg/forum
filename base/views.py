from turtle import pos
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .classes.table_joins import Post_user

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

    print()
    results_list = Post.objects.filter(user=user_id)

    context = {'user_id': user_id, 'username': username, 'posts': results_list}
    return render(request, 'base/myposts.html', context)

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
def deletepost(request):
    user_id = request.user.id
    post_id = request.GET.get('id')
    #post = Post.objects.get(pk=post_id)
    #print(f"user id: {user_id}, post id: {post_id}, post object: {post}")
    print(f"user id: {user_id}, {post_id}")

    context = {'user_id': user_id}
    return render(request, 'base/deletepost.html', context)




#results_list = Post_user.return_user_post_join(user_id)
