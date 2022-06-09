from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, UserProfile, Follow
from .classes.generic_functions import searchbar
from django.db.models import Q
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
    username = request.user.username
    user_id = request.user.id 

    followers = Follow.objects.filter(follower_id=user_id).values('followed_id', 'follower_id')
    followed_id = request.POST.get('followed_id') if request.POST.get('followed_id') != None else ''

    if request.method == "POST":
        if 'unfollow' in request.POST:
            unfollow_instance = Follow.objects.filter(follower_id=user_id).filter(followed_id=followed_id)
            unfollow_instance.delete()
            return redirect('home')
        if 'follow' in request.POST:
            follow_instance = Follow.objects.create(followed_id=followed_id, follower_id=user_id)
            follow_instance.save()
            return redirect('home')


    if posts is None: posts = Post.objects.all()

    if username is None or user_id is None:
        username = "NoUserName"
        user_id = 0

    context = {'posts': posts, 'username': username, 'user_id': user_id, 'followers': followers}
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



"""

    print()
    print(f"request method type { request.method }")
    print(f"follow_binary is : {follow_binary}")
    

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
    logging.debug(f"request.method is: {request.method}")


    level= logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    print()
    logging.debug(" some debug")
    logging.info(" some info")
    logging.error(" some error")

   #all_comments = Comment.objects.filter(post__id=pk).values('id', 'body', 'post_id', 'user_id', 'post__id', 'post__header', 'post__body')
    #all_comments2 = all_comments.filter(user__id=3).values('id', 'body', 'post_id', 'user_id', 'user__id', 'user__username')
  

    mylist = []
    for c in comments:
        for u in users:
            mydict = { "comment_id":c['id'], "comment_body":c['body'], "comment_post_id":c['post_id'], "comment_user_id":c['user_id'], "user_id":u['id'], "user_username":u['username'] } 

            mydict[c['id']] = { c['id']: { "comment_body":c['body'], "comment_post_id":c['post_id'], "comment_user_id":c['user_id'], "user_id":u['id'], "user_username":u['username'] } }
            nested_dict = { 'dictA': {'key_1': 'value_1'},
                            'dictB': {'key_2': 'value_2'}}

            #print(f"user: {u['id']}, {u['username']}. comment: {comment['id']}, {comment['body']}, {comment['post_id']}, {comment['user_id']}")

            #mylist.append(mydict)

    print(mydict)
    #for i in mylist:
    #    print(i)
    #print(mylist[0]['comment_id'])
    #mylist = list(dict.fromkeys(mylist[0]['comment_id']))
    #print(mylist)















    obj = Full_post_comment(comment_id=1, comment_body="test")
    obj2 = Full_post_comment(comment_id=2, comment_body="test22")
    mylist = []

    for c in comments:
        for u in users:
            if c['user_id'] == u['id']:
                full_post_instance = Full_post_comment(comment_id=c['id'], comment_body=c['body'], comment_post_id=pk, comment_user_id=u['id'], user_username=u['username'] )
                mylist.append(full_post_instance)

    print(mylist)
    print()


            #print(f"user: {u['id']}, {u['username']}. comment: {comment['id']}, {comment['body']}, {comment['post_id']}, {comment['user_id']}")

    print()
    for c in comments:
        for u in users:
            if c.user_id == u.id:
                print(f"user: {u.id}, {u.username}. comment: {comment.id}, {comment.body}, {comment.post_id}, {comment.user_id}")
    print()


    he = Full_post_comment(comment_id=1, comment_body="hey", comment_post_id=2, comment_user_id=3, user_id=3, user_username="Nick")
    he2 = Full_post_comment(comment_id=12, comment_body="hey222", comment_post_id=22, comment_user_id=32, user_id=32, user_username="Nick222")

    full_post_list.append(he)   
    full_post_list.append(he2)   
    for i in full_post_list:
        print(i.comment_body, i.comment_id)

    #comments_delete = Comment.objects.filter(post_id=15)
    #comments_delete.delete()

    print()
    for c in comments:
        print(c['id'], c['body'], c['post_id'], c['user_id'])
    print()
    for c in users:
        print(c['id'], c['username'])
    print('-----')

    #users = User.objects.values_list('username', flat=True).filter(Q(comment__user_id=1) & Q(comment__post_id=16))
    #usersORGINAL = User.objects.filter(Q(comment__post_id=pk))
    #users = User.objects.filter(comment__user_id=1).all()

    data = Comment.objects.filter(body='Defo Mafia!').values()
 

"""
