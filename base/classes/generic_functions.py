from django.db.models import Q
from ..models import Post, Follow, Comment
from django.db.models import Count

def searchbar(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(header__icontains=q) |
        Q(body__icontains=q) |
        Q(user__username__icontains=q) 
    )
    return posts

def getFollowedList(user_id):
    followers = Follow.objects.filter(follower_id=user_id).values_list('followed_id', flat=True)
    followed_list = []
    for i in followers:
        followed_list.append(i)
    return followed_list


def userWithMostPosts():
    user_most_posts = Post.objects.select_related('user').values('user_id', 'user__username').annotate(post_count=Count('user_id')).order_by('-post_count')[:1]
    user_most_posts = list(user_most_posts)
    if user_most_posts:
        return user_most_posts[0]
    else:
        return None

def postsWithMostComments():
    post_most_comments = Comment.objects.select_related('post').values( 'post_id', 'post__header', ).annotate(comment_count=Count('post_id')).order_by('-comment_count')[:1]
    post_most_comments = list(post_most_comments)
    if post_most_comments:
        return post_most_comments[0]
    else:
        return None