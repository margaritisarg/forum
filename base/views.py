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

    results_list = Post_user.return_user_post_join(user_id)

    context = {'user_id': user_id, 'username': username, 'posts': results_list}
    return render(request, 'base/post.html', context)







"""
    I will come back to this

    print()
    print(cursor.description)
    for c in cursor.description:
        print(c[0] + '---')
    print()
    print(type(results))
    for r in results:
        print(r)
    print()


"""



