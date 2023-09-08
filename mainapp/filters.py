import django_filters
from django_filters.widgets import RangeWidget, SuffixedMultiWidget
from .models import *
import math


#list_category = Category.objects.filter(name = 'name')

'''
class ShopRangeWidget(SuffixedMultiWidget):
    template_name = 'shop/widgets/rangewidget.html'
    suffixes = ['min', 'max']

    def __init__(self, attrs=None):
        widgets = (forms.TextInput, forms.TextInput)
        super(ShopRangeWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        return [
            num(widget.value_from_datadict(data, files, self.suffixed(name, suffix)))
            for widget, suffix in zip(self.widgets, self.suffixes)
        ]

    # def value_from_datadict(self, data, files, name):
    #     print("vfd %s" % str(data), file=sys.stderr)
    #     return super().value_from_datadict(data, files, name)

    def setRange(self, min_value, max_value):
        step = self.attrs.get('step', 1)
        self.attrs.update({
            'min_value': step * math.floor(min_value / step),
            'max_value': step * math.ceil(max_value / step)
        })
'''


class Filter_products(django_filters.FilterSet):



	price = django_filters.RangeFilter(widget=RangeWidget(attrs={'step': 100, }))
	title = django_filters.CharFilter(lookup_expr='icontains')
	#name = django_filters.CharFilter(lookup_expr='icontains')
	
#	category = django_filters.ChoiceFilter(choices = 'list_category')
#	price__min = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#	price__max = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

	class Meta:
		model = Product
		fields = ['title', 'price', 'category']




