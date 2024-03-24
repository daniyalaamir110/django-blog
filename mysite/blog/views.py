from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post

def post_list(request):
    posts = get_list_or_404(Post, status=Post.Status.PUBLISHED)
    return render(
        request=request, 
        template_name='blog/post/list.html', 
        context={'posts': posts}
    )


# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
#     return render(
#         request=request, 
#         template_name='blog/post/detail.html', 
#         context={'post': post}
#     )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED
    )
    return render(
        request=request, 
        template_name='blog/post/detail.html', 
        context={'post': post}
    )