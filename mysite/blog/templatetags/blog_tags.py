from django import template
from django.utils.safestring import mark_safe
from ..models import Post
from markdown import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.most_commented.all()[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown(text))