from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db import connection, connections
from .classes.table_joins import Post_joined_user

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
    
    if username is None and user_id is None:
        username = "NoUserName"
        user_id = 0

    context = {'posts': posts, 'username': username, 'user_id': user_id}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def post(request):
    user_id = request.user.id 
    username = request.user.username

    cursor = connection.cursor()
    cursor.execute(f"SELECT  a.[username], b.[header], b.[body] FROM ( SELECT [header], [body], [user_id] FROM base_post WHERE user_id = {user_id} ) b INNER JOIN auth_user a ON b.user_id = a.id")
    results = cursor.fetchall()

    results_list = []
    for result in results:
        post_joined_user = Post_joined_user()
        post_joined_user.user = result[0]
        post_joined_user.header = result[1]
        post_joined_user.body = result[2]
        results_list.append(post_joined_user)

    context = {'user_id': user_id, 'username': username, 'results_list': results_list}
    return render(request, 'base/post.html', context)







"""
    query = Post.objects.select_related('user').filter(user__id__iexact=1)

    print()
    print()
    print(type(query))
    print(query)
    print(type(query))
    print(query.query)
    print()

    for e in query.all():
        print(e)
        #print(e.auth_useris_active)

    print()
    print()


"""



