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



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'slug', 'price']
     
    list_editable = ['price']





admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
#admin.site.register(CartProduct)
#admin.site.register(Cart)
admin.site.register(Customer)
#admin.site.register(Order)

admin.site.register(News)





