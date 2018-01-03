from .models import Post
from django.shortcuts import render, get_object_or_404
# from django.views.generic import ListView
from django.core.paginator import Paginator
# from django.views.generic.dates import YearArchiveView
import re

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


posts = Post.objects.all().filter(status='published')


def tag_archive_data(posts):
    """create a list for tag and its counts"""
    count_list = []
    count = {}
    for post in posts:
        # tag = post.tag
        tag_list = re.split(", ", post.tag)
        for tag in tag_list:
            if tag not in count:
                count[tag] = 1
            else:
                count[tag] += 1
    for k, v in sorted(count.items(), reverse=True):
        count_list.append({'tag': k, 'count': v})
    return count_list


def year_archive_data(posts):
    """create a list for year and the posts count"""
    count_list = []
    count = {}
    for post in posts:
        year = post.publish.year
        if year not in count:
            count[year] = 1
        else:
            count[year] += 1
    for k, v in sorted(count.items(), reverse=True):
        count_list.append({'year': k, 'count': v})
    return count_list


def sidebar_data():
    """combine tag_count and year_archive_count data into one single function"""
    tag_count = tag_archive_data(posts)
    year_count = year_archive_data(posts)
    data = {'tag_count': tag_count, 'year_count': year_count}
    return data


# using Paginator for post list page
def post_list(request):
    sidebardata = sidebar_data()
    posts = Post.objects.all().filter(status='published')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/list.html', {'posts': posts,
                                              'tag_count': sidebardata['tag_count'],
                                              'year_count': sidebardata['year_count']})


def post_detail(request, year, month, day, slug):
    sidebardata = sidebar_data()
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='published') # only display the post detail for published posts
    return render(request, 'blog/detail.html', {'post': post,
                                                'tag_count': sidebardata['tag_count'],
                                                'year_count': sidebardata['year_count']})


def post_year_archive(request, year):
    sidebardata = sidebar_data()
    posts = Post.objects.all().filter(publish__year=year)
    return render(request, 'blog/post_archive_year.html', {"posts": posts,
                                                           "year": year,
                                                           'tag_count': sidebardata['tag_count'],
                                                           'year_count': sidebardata['year_count']})


def tag_view(request, tag):
    sidebardata = sidebar_data()
    tag_posts = []
    for post in posts:
        tag_list = re.split(", ", post.tag)
        if tag in tag_list:
            tag_posts.append(post)

    # tag_posts = Post.objects.all().filter(tag=tag)
    # tag_posts = get_object_or_404(Post, tag=tag)
    paginator = Paginator(tag_posts, 5)
    page = request.GET.get('page')
    tag_posts = paginator.get_page(page)
    return render(request, 'blog/tag_view.html', {"posts": tag_posts,
                                                  'tag_count': sidebardata['tag_count'],
                                                  'year_count': sidebardata['year_count']})

