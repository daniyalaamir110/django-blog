from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

def post_list(request):
    post_list = Post.published.all()
    
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page', 1)

    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    # Shorthand version
    # posts = paginator.get_page(page)

    return render(
        request=request, 
        template_name='blog/post/list.html', 
        context={'posts': posts}
    )

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