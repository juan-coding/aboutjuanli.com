from blog.models import Post
from django.shortcuts import render, get_object_or_404
# from django.views.generic import ListView
from django.core.paginator import Paginator
import re
from blog.forms import EmailSharePostForm
from django.urls import reverse
from django.core.mail import send_mail


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

# this 'posts' variable will be used inside the functions
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


def post_data():
    """combine tag_count and year_archive_count data into one single function"""
    tag_count = tag_archive_data(posts)
    year_count = year_archive_data(posts)
    data = {'posts': posts,
            'tag_count': tag_count,
            'year_count': year_count,
            'body_title': ""}
    return data


# using Paginator for post list page
def post_list(request):
    data = post_data()
    # posts = Post.objects.all().filter(status='published')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)
    data.update({'posts': post_list, 'body_title': 'All posts in this blog'})
    return render(request, 'blog/post/list.html', data)


def post_year_archive(request, year):
    data = post_data()
    post_list = Post.objects.all().filter(publish__year=year)
    # post_list = get_object_or_404(Post, publish__year=year, status='published')
    # get_object_or_404 used to return a single post
    data.update({'posts': post_list, 'body_title': 'Posts for {}'.format(year)})
    return render(request, 'blog/post/list.html', data)


def post_detail(request, year, month, day, slug):
    data = post_data()
    post_list=[]
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='published')
    post_list.append(post)
    data.update({"posts": post_list})
    return render(request, 'blog/post/detail.html', data)
    # return render(request, 'blog/detail.html', {'posts': posts,
    #                                             'tag_count': sidebardata['tag_count'],
    #                                             'year_count': sidebardata['year_count']})


def tag_view(request, tag):
    data = post_data()
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
    data.update({"posts": tag_posts, 'body_title': 'Posts for tag: {}'.format(tag)})
    return render(request, 'blog/post/list.html', data)
    # return render(request, 'blog/tag_view.html', {"posts": tag_posts,
    #                                               'tag_count': sidebardata['tag_count'],
    #                                               'year_count': sidebardata['year_count']})


def share_post(request, post_id):
    # get_object_or_404 return a single post, so use it in this function
    post = get_object_or_404(Post,
                             id=post_id,
                             status='published')
    sent = False

    if request.method == 'POST':
        form = EmailSharePostForm(request.POST)
        if form.is_valid():
            from django.urls import reverse
            post_url = request.build_absolute_uri(reverse('post_detail', args=(post.publish.year, post.publish.month,
                                                                               post.publish.day,post.slug)))
            cd = form.cleaned_data
            name = cd['name']
            from_email = cd['email']
            to_email = cd['to']
            comment = cd['comment']
            subject = '{} ({}) recommends you reading "{}"'.format(name, from_email, post.title)
            message = "Read '{}' at {}. {}'s comments: {}".format(post.title, post_url, name, comment)
            send_mail(subject, message, from_email, [to_email])
            sent = True
    else:
        form = EmailSharePostForm()
    return render(request, 'blog/share/share_post.html', {'post': post,
                                                         'form': form,
                                                         'sent': sent})













