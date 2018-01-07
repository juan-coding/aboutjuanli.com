from django.contrib.syndication.views import Feed
from blog.models import Post
from django.template.defaultfilters import truncatewords, safe


class LatestPostsFeed(Feed):
    title = "aboutjuanli.com Blog"
    link = "/blog/"
    description = "New posts of my blog"

    def items(self):
        return Post.published.order_by('-publish')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return safe(truncatewords(item.body, 30))

