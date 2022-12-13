from django.shortcuts import render
from .models import Post
# Create your views here.
def index(request):
    posts = Post.objects.all()
    print(posts)
    context = {
        'Posts':posts
    }
    return render(request, 'documentation/index.html', context)
