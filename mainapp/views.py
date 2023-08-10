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

from rest_framework import generics

from .serializer import ProductSerializer

from .filters import Filter_products
from .models import Category, Product, Customer, News

#from .mixins import CartMixin
#from .forms import OrderForm
#from .utils import recalc_cart 

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



'''
def other_page(request, page):
    try:
        template = get_template(page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


'''


                            # представление кантактов (страница о нас)

class ContactView( View):

    def get(self, request, *args, **kwargs):
            
        categories = Category.objects.all()
         
        context = {
            'categories': categories
                        
        }
        return render(request, 'mainapp/contact.html', context)

                            



def getnews(request):
            

    news_post = News.objects.all() [::-1]
    paginator = Paginator(news_post, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
         
    context = {

        'news_post' : news_post,
        'paged_products': paged_products
            
                        
    }
    return render(request, 'mainapp/blog.html', context)
               


                            #представление главной страницы
class BaseView( View):

  
    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all()
        products = Product.objects.all() [:5:-1]
        news_post = News.objects.all() [:4:-1]
        
       
        context = {
            'categories': categories,
            'products' : products,
            'news_post' : news_post
        }
        
        print('запуск главное страницы')
        return render(request, 'mainapp/index.html', context)
                            


                            #представление страници всех категорий (каталог категорий)


                             

                            #каталог категорий товаров 
class AllCategoryView( View): 
    

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        



        context = {
            'categories': categories
                        
        }
        return render(request, 'mainapp/all_category.html', context)



                            
                            #представление страници одного продукта 
class ProductDetailView(DetailView):
    model = Product

    def product_detail(request, id, slug):

            products = get_object_or_404(Product, id=id, slug=slug, available=True)
            context = {
                
            
            'products' : products
            } 

            render(request, 'mainapp/product_detail.html', context)


                            
class ProductApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 



                            #представление поиска 

class SearchView(View):

    model = Product 

    def get(self, request):

        query = request.GET.get('q')

        products = Product.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
        #filter_P = Filter_products(self.request.GET, queryset=products)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
             #'filter_P': filter_P
            'products': products,
            'paged_products': paged_products
        }


        return render(request, 'mainapp/search.html', context)






class PageFilterView(View):

    model = Product

    def filter(self, request):
        products_filter = Product.objects.all()
        filter_P = Filter_products(self.request.GET, queryset=products_filter)

        context = {
            'filter_P': filter_P
        }

        return render(request, 'mainapp/pageproductfilter.heml', context)



'''
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['filter_P'] = Filter_products(self.request.GET, queryset=self.get.queryset())
        return context
'''

                                #представление корзины (старое)

'''
class AddToCartView(View):

    def get(self, request, *args, **kwargs):

        #product_id, product_slug = kwargs.get('id'), kwargs.get('slug') 

        
        #product_iden = Product.objects.get(product_id)
        #product = product_iden.model_class().objects.get(slug=product_slug)
        print(Product.price)

        #content_type = ContentType.objects.get(model=product_id)
        #product = content_type.model_class().objects.get(slug=product_slug)
                                                                                    #product_id=product,
        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart, final_price=Product.objects.filter('price')

        if created:
            self.cart.product.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        

        return HttpResponseRedirect('mainapp/cart/')

class DeleteFromCartView(View):

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

class ChangeQTYView(View):

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

class CartView(View):

    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'mainapp/cart/', context)


class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)

class MakeOrderView(View):

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
   

'''


#filter_P.qs,
        #paginator = Paginator(products, 4)
        #page = request.GET.get('page')
  #paged_products = paginator.get_page(page)
           #'paged_products' : paged_products,
            #'products': products,

                                           
        
      
       