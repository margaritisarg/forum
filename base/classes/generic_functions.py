from django.db.models import Q
from ..models import Post

def searchbar(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(header__icontains=q) |
        Q(body__icontains=q) |
        Q(user__username__icontains=q) 
    )
    return posts