#from django.shortcuts import render

# Create your views here.


#def test_view(request):
#	return render(request, 'base.html', {} )
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import DetailView, View, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 


from .models import Category, Product, Customer, Cart, CartProduct, News
from .mixins import CartMixin
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




class ContactView( CartMixin, View):

    def get(self, request, *args, **kwargs):
            
        categories = Category.objects.all()
         
        context = {
            'cart': self.cart,
            'categories': categories
                        
        }
        return render(request, 'mainapp/contact.html', context)


class NewsView( CartMixin, View):

    def get(self, request, *args, **kwargs):
            
        categories = Category.objects.all()
        news_post = News.objects.all()
         
        context = {
            'cart': self.cart,
            'categories': categories,
            'news_post' : news_post
            
                        
        }
        return render(request, 'mainapp/blog.html', context)


class BaseView( CartMixin, View):

  
    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all()
        products = Product.objects.all()
        news_post = News.objects.all()
        
       
        context = {
            'categories': categories,
            'cart': self.cart,
            'products' : products,
            'news_post' : news_post
        }
        
        print('запуск главное страницы')
        return render(request, 'mainapp/index.html', context)

class AllCategoryView( CartMixin, View): #каталог категорий товаров
    

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        



        context = {
            'cart': self.cart,
            'categories': categories
                        
        }
        return render(request, 'mainapp/all_category.html', context)


class ProductListView(DetailView, CartMixin):
    model = Category
    
    def product_list(request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.filter(category=category)
        return render(request, 'mainapp/category_detail', {'products': products, 'category': category, 'categories': categories,  'cart': self.cart})



class ProductDetailView(DetailView, CartMixin):
    model = Product

    def product_detail(request, id, slug):

            products = get_object_or_404(Product, id=id, slug=slug, available=True)
            context = {
                
            'cart': self.cart,
            'products' : products
            } 

            render(request, 'mainapp/product_detail.html', context)


        


'''
class CategoryDetailView( DetailView, CartMixin):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart'] = self.cart


        return context

'''

class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        product_id, product_slug = kwargs.get('id'), kwargs.get('slug') 

        product = Product.objects.get(id=request.GET.get('id'))
        #product_iden = Product.objects.get(product_id)
        #product = product_iden.model_class().objects.get(slug=product_slug)
        print(Product.price)

        #content_type = ContentType.objects.get(model=product_id)
        #product = content_type.model_class().objects.get(slug=product_slug)
       
        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart, product_id=product, final_price=product.price)

        if created:
            self.cart.product.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        

        return HttpResponseRedirect('mainapp/cart/')

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('id'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.product.remove(cart_product)

        cart_product.delete()

        recalc_cart(self.cart)

       
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('mainapp/cart')

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('id'), kwargs.get('slug')
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

        return HttpResponseRedirect('mainapp/cart/')

class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'mainapp/cart/', context)


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
   

class SearchView(CartMixin , View):

    model = Product

    def get(self, request, *args, **kwargs):

       
        query = self.request.GET.get('q')

        products = Product.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
        categories = Category.objects.all()

        context = {
            'categories': categories,
            'cart': self.cart,
            'products' : products
            
        }
        
        return render(request, 'mainapp/search.html', context)
        
      
       