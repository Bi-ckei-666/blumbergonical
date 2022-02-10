from django import forms
from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin


from .models import *



# Register your models here.


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
'''
class SubNotebookAdmin(admin.ModelAdmin):	
	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Notebook'))
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)
'''

class SmartphoneAdmin(admin.ModelAdmin):	

	change_form_template =  'admin.html'
	form = SmartphoneAdminForm
	
	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Smartphone'))
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)

class LightingAdmin(admin.ModelAdmin):	


	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Lighting'))
		elif db_filed.name == 'sub_categor':
			return ModelChoiceField(SubCat.objects.filter(slug='Lamps'))
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)

class NonStationaryWireAdmin(admin.ModelAdmin):

	def formfield_for_foreignkey(self, db_filed, request, **kwargs):
		if db_filed.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='Nonstationarywire'))
			
		return super().formfield_for_foreignkey(db_filed, request, **kwargs)





admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Lighting, LightingAdmin)
admin.site.register(NonStationaryWire, NonStationaryWireAdmin)




