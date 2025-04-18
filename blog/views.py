from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404


# Create your views here.
def post_list_view(request):
    posts_list = Post.objects.filter(status=Post.STATUS_CHOICES[0][0])
    return render(request, 'blog/posts_list.html', {'posts_list': posts_list})


def details_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
