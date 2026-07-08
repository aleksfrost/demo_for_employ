from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News

class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return News.objects.filter(is_active=True)

    def lastmod(self, obj:News):
        return obj.published_at

    def location(self, obj: News):
        return reverse('news_detail', args=[obj.slug])

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['news_list', 'login', 'register']

    def location(self, item):
        return reverse(item)