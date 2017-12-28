from .models import Post
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    context_object_name = 'posts'
    template_name = 'blog/list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)
    return render(request, 'blog/detail.html', {'post': post})