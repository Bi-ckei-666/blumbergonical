from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View




from .models import Category, Customer, Cart, Notebook, Smartphone, Lighting, NonStationaryWire

class CategoryDetailMixin(SingleObjectMixin):

	CATEGORY_SLUG2PRODUCT_MODEL = {
		'Notebook': Notebook,
		'Smartphone': Smartphone,
		'lighting': Lighting,
		'Nonstationarywire': NonStationaryWire
		
	}
	
	def get_context_data(self, **kwargs):	

		if isinstance(self.get_object(), Category):
			model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
			context = super().get_context_data(**kwargs)
			context['categories'] = Category.objects.all()
			context['category_products'] = model.objects.all()
			return context	
	
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.filter(slug = 'name')
		return context
       
class CartMixin(View):

	def dispatch(self, request, *args, **kwargs):

		if request.user.is_authenticated:
			customer = Customer.objects.filter(user=request.user).first()
			if not customer:
				customer = Customer.objects.create(user=request.user)
			cart = Cart.objects.filter(owner=customer).first()

			if not cart:
				cart = Cart.objects.create(owner=customer)
				
		else:
			
			cart = Cart.objects.filter(for_anonymous_user=True).first()
			if not cart:
				cart = Cart.objects.create(for_anonymous_user=True)

		self.cart = cart
		
		return super().dispatch(request, *args, **kwargs)
			


# Послание в миксынах!!!