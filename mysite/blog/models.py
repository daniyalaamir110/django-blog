from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

    
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self)\
            .get_queryset()\
            .filter(status=Post.Status.PUBLISHED)
    

class MostCommentedManager(models.Manager):
    def get_queryset(self):
        return super(MostCommentedManager, self)\
            .get_queryset()\
            .filter(status=Post.Status.PUBLISHED)\
            .annotate(total_comments=models.Count('comments'))\
            .order_by('-total_comments')
    

class Post(models.Model):


    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    # slug = models.SlugField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts'
    )
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()
    most_commented = MostCommentedManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[self.id])

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])
    
    def get_similar_posts(self):
        post_tags_ids = self.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=self.id)
        similar_posts = similar_posts.annotate(same_tags=models.Count('tags')).order_by('-same_tags', '-publish')[:4]
        return similar_posts


class Comment(models.Model):
    """
    Model for comments on blog posts.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'