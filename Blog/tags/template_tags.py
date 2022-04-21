from django import template
from django.shortcuts import get_object_or_404
from core.views import Post

register = template.Library()


@register.simple_tag
def get_post_liked_user(pk, attr):
    obj = getattr(Post.liked_by.objects.get(pk=int(pk)), attr)
    return obj
