from django.urls import path
from . import views
from .views import (
    BaseView, 
    ProductDetailView,
    ContactView,
    AllCategoryView,
    SearchView
    )   

#from mainapp import views

app_name = 'mainapp'



urlpatterns = [
    path('', BaseView.as_view(), name='index.html'),
    path('search', SearchView.as_view(), name='search'),
    path('products/<id>/<slug>/', ProductDetailView.as_view(), name='product_detail'),
    #path('cart/', CartView.as_view(), name='cart'),
    #path('add-to-cart/<str:id>/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
    #path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    #path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    #path('checkout/', CheckoutView.as_view(), name='checkout'),
    #path('make-order/', MakeOrderView.as_view(), name='make_order'),
    
    path('contact/', ContactView.as_view(), name='contact'),
    path('all_category/', AllCategoryView.as_view(), name='all_category'),
    path('blog/', views.getnews, name='blog')
    
]


#path('search/', SearchView.as_view(), name='search'),



