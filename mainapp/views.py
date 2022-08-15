#from django.shortcuts import render

# Create your views here.


#def test_view(request):
#	return render(request, 'base.html', {} )
from django.db import transaction
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import DetailView, View, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 


from .models import Category, Category_1, Product, Customer, Cart, CartProduct, NonStationaryWire, LatestProducts, Lampa, News
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm
from .utils import recalc_cart 

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


'''
def other_page(request, page):
    try:
        template = get_template(page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


'''




class ContactView(CategoryDetailMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
            
        categories = Category.objects.all()
         
        context = {
            'cart': self.cart,
            'categories': categories
                        
        }
        return render(request, 'contact.html', context)





class BaseView(CategoryDetailMixin, CartMixin, View):

  
    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all()
        products = Product.objects.all()
        product_for_main_page = LatestProducts.objects.get_products_for_main_page('nonstationarywire', 'lampa')
        news_post = News.objects.order_by('title')[:2]
        
       
        context = {
            'categories': categories,
            'cart': self.cart,
            'products' : products,
            'product_for_main_page' : product_for_main_page,
            'news_post' : news_post
        }
        print(len(product_for_main_page))
        print(product_for_main_page)
        return render(request, 'base.html', context)

class AllCategoryView(CategoryDetailMixin, CartMixin, View): #каталог категорий товаров
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        news_post = News.objects.order_by('title')[:2]

        context = {
            'cart': self.cart,
            'categories': categories,
            'news_post' : news_post
                        
        }
        return render(request, 'all_category.html', context)

class ProductDetailView(CategoryDetailMixin, DetailView, CartMixin):

    CT_MODEL_MODEL_CLASS = {
        'nonstationarywire': NonStationaryWire,
        'lampa': Lampa

    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart 
        context['categories'] = Category.objects.all()
        
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView, CartMixin):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart'] = self.cart


        return context

class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
      
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
       
        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id, final_price=product.price)
       
       
        if created:
            self.cart.product.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect('/cart/')

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.product.remove(cart_product)

        cart_product.delete()

        recalc_cart(self.cart)

       
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")

        return HttpResponseRedirect('/cart/')

class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)

class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            recalc_cart(self.cart)
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')
   

class SearchView(CategoryDetailMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
            
        categories = Category.objects.all()
        
        context = {
            'cart': self.cart,
            'categories': categories
            }
        return render(request, 'search.html', context)



