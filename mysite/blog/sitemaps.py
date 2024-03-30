from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority= 0.9

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated

    # For lastmod
    # def updated(self, obj):
    #     return obj.updated
    
    # For location
    # def location(self, obj):
    #     return obj.get_absolute_url()