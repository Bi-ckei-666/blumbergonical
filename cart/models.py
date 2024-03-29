from django.db import models

from mainapp.models import Product
from accounts.models import Account
from mainapp.models import Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзина пользователя'


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине пользователя'
    