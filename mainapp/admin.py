from django import forms
from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *



# Register your models here.


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)	

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs, Product, 'category', 'products_count', cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

'''
class SmartphoneAdminForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		instance = kwargs.get('instance')
		if instance and not instance.sd:
			self.fields['sd_volume'].widget.attrs.update({'readonly': True, 'style': 'background: lightgray;'})
	def clean(self):
		if not self.cleaned_data['sd']:
			self.cleaned_data['sd_volume'] = None
		return self.cleaned_data



class NotebookAdmin(admin.ModelAdmin):	
	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Notebook'))
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)

class SubNotebookAdmin(admin.ModelAdmin):	
	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Notebook'))
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):	

	change_form_template =  'admin.html'
	form = SmartphoneAdminForm
	
	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Smartphone'))
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)
'''


class NonStationaryWireAdmin(admin.ModelAdmin):

	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Wire'))

class LampaAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Lamps'))
			
	




admin.site.register(Category, CategoryAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(NonStationaryWire, NonStationaryWireAdmin)
admin.site.register(Lampa, LampaAdmin)
admin.site.register(News)





