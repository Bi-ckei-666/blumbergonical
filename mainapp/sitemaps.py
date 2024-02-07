from django.contrib import sitemaps
from django.urls import reverse

from .models import *



class ProductSitemap(sitemaps.Sitemap):

	priority = 0.5

	def items(self):
		return Product.objects.all()
	

class StaticViewSitemap(sitemaps.Sitemap):
	priority = 0.5

	def items(self):
		return ["mainapp:contact"]

	def location(self, item):
		return reverse(item)