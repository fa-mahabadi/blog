import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse
from .models import Post


class LastestPostFeed(Feed):
    title = "My Blog"
    description = "New post of my blog"

    def link(self):
        return reverse("blog:post_list")

    def items(self):
        # return Post.published.all()[:3]
        return Post.published.filter(tags__isnull=False).distinct()[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
