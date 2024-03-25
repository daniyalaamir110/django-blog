from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment, Post
from .forms import CommentForm, EmailPostForm

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request=request, 
        template_name='blog/post/detail.html', 
        context={'post': post, 'comments': comments, 'form': form}
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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(
        request=request,
        template_name='blog/post/share.html',
        context={'post': post, 'form': form, 'sent': sent}
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    comments = post.comments.filter(active=True)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        form = CommentForm()
    
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post, 'comment': comment, 'comments': comments, 'form': form}
    )
