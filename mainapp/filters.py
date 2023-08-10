import django_filters

from .models import *



class Filter_products(django_filters.FilterSet):

	price = django_filters.RangeFilter()
	
#	price__min = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#	price__max = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

	class Meta:
		model = Product
		fields = ['price', 'title']






