from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm



# Create your views here.

class PostListView(generic.ListView):
    # model = Post
    context_object_name = 'posts_list'
    template_name = 'blog/posts_list.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.STATUS_CHOICES[0][0]).order_by('-datetime_modified')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = "blog/post_create.html"


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('posts_list')

    # def get_success_url(self):
    #     return reverse('posts_list')

######################################################################## Functional view ##############################
# def post_list_view(request):
#     posts_list = Post.objects.filter(status=Post.STATUS_CHOICES[0][0]).order_by('-datetime_modified')
#     return render(request, 'blog/posts_list.html', {'posts_list': posts_list})


# def details_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})


# def add_new_post_view(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('posts_list')
#     else:
#         form = PostForm()
#     return render(request, "blog/post_create.html", {'form': form})


# def update_post_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(request.POST or None, instance=post)
#
#     if form.is_valid():
#         form.save()
#         return redirect('posts_list')
#
#     return render(request, "blog/post_create.html", {'form': form})


# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('posts_list')
#     return render(request, 'blog/post_delete.html', {'post': post})
