from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

# custom template tags

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/lastest_post.html")
def show_lastest_posts():
    lastest_posts = Post.published.order_by("-publish")[:5]
    return {"lastest_posts": lastest_posts}


@register.simple_tag
def get_most_commented_post():
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:3]


# custom template filters
@register.filter(name="markdown")
def markdown_format(txt):
    return mark_safe(markdown.markdown(txt))
