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
    paginator = Paginator(news_post, 2)
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
        
        products = Product.objects.all() [:5:-1]
        news_post = News.objects.all() [:4:-1]
        
       
        context = {
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
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products': products,
            'paged_products': paged_products
        }

        return render(request, 'mainapp/search.html', context)


class PageFilterView(View):

    model = Product

    def get(self, request):
        products_filter = Product.objects.all()
        filter_P = Filter_products(self.request.GET, queryset=products_filter)

        context = {
            'filter_P': filter_P
        }

        return render(request, 'mainapp/pageproductfilter.html', context)


def postorder(request):

    return render(request, 'mainapp/order_post.html')
         