from .models import Post
from django.shortcuts import render, get_object_or_404
# from django.views.generic import ListView
from django.core.paginator import Paginator


# class PostListView(ListView):
#     model = Post
#     queryset = Post.objects.all().filter(status='published')
#     # list all the published posts in page using Paginator class
#     # or filter the number of posts displayed in pages (up to personal favourite)
#     context_object_name = 'posts'
#     template_name = 'blog/list.html'


# def post_list(requset):
#     posts = Post.objects.all().filter(status='published')
#     return render(request, 'blog/list.html', {'posts': post})


# using Paginator in a view
def post_list(request):
    posts = Post.objects.all().filter(status='published')
    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/listing.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='published') # only display the post detail for published posts
    return render(request, 'blog/detail.html', {'post': post})