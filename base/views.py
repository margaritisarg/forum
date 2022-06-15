from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, UserProfile, Follow
from .classes.generic_functions import searchbar, getFollowedList, userWithMostPosts, postsWithMostComments
import logging

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
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

def userprofile(request, pk):
    user_profile = UserProfile.objects.filter(user__id=pk).values('id', 'description', 'user_id', 'user__username')
    user_followers = Follow.objects.filter(followed_id=pk).values('id', 'followed_id', 'follower_id')

    user_followers_count = user_followers.count()

    context = {'user_profile': user_profile[0], 'user_follower_count': user_followers_count}
    return render(request, 'base/user_profile.html', context)


def home(request):
    posts = searchbar(request)
    
    followed_id = request.POST.get('followed_id') if request.POST.get('followed_id') != None else ''

    if request.method == "POST":
        if 'unfollow' in request.POST:
            unfollow_instance = Follow.objects.filter(follower_id=request.user.id).filter(followed_id=followed_id)
            unfollow_instance.delete()
            return redirect('home')
        if 'follow' in request.POST:
            follow_instance = Follow.objects.create(followed_id=followed_id, follower_id=request.user.id)
            follow_instance.save()
            return redirect('home')
    

    followed_list = getFollowedList(request.user.id)
    user_most_posts = userWithMostPosts()
    post_most_comments = postsWithMostComments()

    context = {'posts': posts, 'followed_list': followed_list, 'user_most_posts': user_most_posts, 'post_most_comments': post_most_comments}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def followedposts(request):
    user_id = request.user.id 
    username = request.user.username

    followers = Follow.objects.filter(follower_id=user_id).values_list('followed_id', flat=True)
    followed_list = []
    for i in followers:
        followed_list.append(i)
    
    print()
    print(followed_list)
    posts = Post.objects.filter(user_id__in=followed_list)
    print(posts)
    print()

    context = {'posts': posts}
    return render(request, 'base/followed_posts.html', context)

@login_required(login_url='login')
def myposts(request):
    user_id = request.user.id 
    username = request.user.username

    results_list = Post.objects.filter(user=user_id)
    context = {'user_id': user_id, 'username': username, 'posts': results_list}

    return render(request, 'base/myposts.html', context)


def commentspost(request, pk):
    post = Post.objects.filter(id=pk)
    users = User.objects.filter(comment__post_id=pk).values('id')

    user_id_list = []
    for u in users:
        user_id_list.append(u['id'])

    user_id_list = list(set(user_id_list))

    all_comments = Comment.objects.filter(post__id=pk).filter(user__id__in=user_id_list).values('id', 'body', 'post_id', 'user_id', 'user__id', 'user__username')

    context = {'posts': post, 'comments_list':all_comments}

    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        delete_comment = request.POST.get('delete_comment')
        if 'delete_comment' == delete_comment:
            comment = Comment.objects.filter(id=comment_id)
            comment.delete()
            return redirect('commentspost', pk=pk)
        else:
            comment = request.POST["user_comment"]
            comment_instance = Comment.objects.create(body=comment, post_id=pk, user_id=request.user.id)
            comment_instance.save()
            return redirect('commentspost', pk=pk)
    else:
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


