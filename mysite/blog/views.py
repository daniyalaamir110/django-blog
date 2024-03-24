from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
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


class PostListView(ListView):
    """
    Class-based view for listing posts.
    Alternative to the function-based view post_list.
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# def post_detail(request, id):
#     post = get_object_or_404(
#         Post,
#         id=id,
#         status=Post.Status.PUBLISHED
#     )
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


class PostDetailView(DetailView):
    """
    Class-based view for viewing a single post.
    Alternative to the function-based view post_detail.
    """

    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'post'
    query_pk_and_slug = True
    # pk_url_kwarg = 'id'
    # pk_url_kwarg = 'pk'
    # pk_url_kwarg = 'post