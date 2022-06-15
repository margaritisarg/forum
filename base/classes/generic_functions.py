from django.db.models import Q
from ..models import Post, Follow

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