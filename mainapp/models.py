


from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone




from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()
# Create your models here.

#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order

#***********

#6 Customer
#7 Specification


def get_models_for_count(*model_names):
	return [models.Count(model_name) for model_name in model_names]

def get_product_url(obj, viewname):
    product_id = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'product_id': obj.id, 'slug': obj.slug})



class MinResalutionErrorException():
	pass


class MaxResalutionErrorException():
	pass






class Category(MPTTModel):

	name = models.CharField(max_length=255, verbose_name="имя категории")
	slug = models.SlugField(unique=True)
	#objects = CategoryManager()
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

	class MPTTMeta:
		order_insertion_by = ['name']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'slug': self.slug})

	class Meta:
		verbose_name = 'Категорию'
		verbose_name_plural = 'категории'

class Product(models.Model):

	
	category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
	title = models.CharField(max_length=255, verbose_name="наименование")
	identifications = models.PositiveIntegerField(default=1, verbose_name='индификатор', blank=True)
	slug = models.SlugField(unique=True)
	image = models.ImageField(verbose_name='Изображение')
	description = models.TextField(verbose_name='описание', null=True)
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
	articl = models.IntegerField(blank=True, null=True ,verbose_name='артикул')
	count_view = models.PositiveIntegerField(default=0, verbose_name='Количество')
	availabillity = models.BooleanField(null=True, verbose_name="наличие")
	brand = models.CharField(max_length=255, verbose_name="Брэнд", blank=True)
	strana = models.CharField(max_length=255, verbose_name="Страна производитель", blank=True)
	shtrih_code = models.CharField(max_length=255, verbose_name="Штрих-код", blank=True)

	characteristiks = models.TextField(verbose_name='описание', null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add = True)
	property1 = models.CharField(max_length=255, verbose_name="свойство_№1", blank=True)
	property2 = models.CharField(max_length=255, verbose_name="свойство_№2", blank=True)
	property3 = models.CharField(max_length=255, verbose_name="свойство_№3", blank=True)
	property4 = models.CharField(max_length=255, verbose_name="свойство_№4", blank=True)
	property5 = models.CharField(max_length=255, verbose_name="свойство_№5", blank=True)
	property6 = models.CharField(max_length=255, verbose_name="свойство_№6", blank=True)
	property7 = models.CharField(max_length=255, verbose_name="свойство_№7", blank=True)
	property8 = models.CharField(max_length=255, verbose_name="свойство_№8", blank=True)
	property9 = models.CharField(max_length=255, verbose_name="свойство_№9", blank=True)
	property10 = models.CharField(max_length=255, verbose_name="свойство_№10", blank=True)

	def __str__(self):
		return self.title

	def get_model_name(self):
		return self.__class__.__name__.lower()

	def get_absolute_url(self):
		return reverse('mainapp:product_detail', args=[self.id, self.slug])

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'





class Customer(models.Model):


	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
	phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
	address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
	

	def __str__(self):
		return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

	class Meta:
		verbose_name = 'Покупателя'
		verbose_name_plural = 'Покупатели'


class News(models.Model): #модель для написания постов на главное странице
	title = models.CharField(max_length=255, verbose_name='Наименование новости')
	image = models.ImageField(verbose_name='Изображение')
	description = models.TextField(verbose_name='текст новости', null=True)
	date_created = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'


class Variation(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variation_value = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.variation_value


'''
class CartProduct(models.Model):

	user = models.ForeignKey('Customer', null=True, verbose_name='Покупатель', on_delete=models.CASCADE)
	cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name="related_products")
	product_id = models.PositiveIntegerField()
	#content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	#object_id = models.PositiveIntegerField()
	#content_object = GenericForeignKey('content_type', 'object_id')
	qty = models.PositiveIntegerField(default=1)
	final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая Цена')

	#def __str__(self):
	#	return "Продукт: {} (для корзины)".format(self.content_object.title)

	def save(self, *args, **kwargs):
		self.final_price = self.qty * self.content_object.price
		super().save(*args, **kwargs)

	def get_model_name(self, *args, **kwargs):
		return self.__class__._meta.model_name

	class Meta:
		verbose_name = 'Товары в корзине'
		verbose_name_plural = 'Товары в корзине'


class Cart(models.Model):

	owner = models.ForeignKey('Customer', null=True, verbose_name='Покупатель', on_delete=models.CASCADE)
	product = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
	total_product = models.PositiveIntegerField(default=0)
	final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая Цена')
	in_order = models.BooleanField(default=False)
	for_anonymous_user = models.BooleanField(default=False)
	


	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Корзину'
		verbose_name_plural = 'Корзина'


'''
	



 
'''

class Order(models.Model):

	STATUS_NEW = 'new'
	STATUS_IN_PROGRESS = 'in_progress'
	STATUS_READY = 'is_ready'
	STATUS_COMPLETED = 'completed'

	BUYING_TYPE_SELF = 'self'
	BUYING_TYPE_DELIVERY = 'delivery'

	STATUS_CHOICES = (
		(STATUS_NEW, 'Новый заказ'),
		(STATUS_IN_PROGRESS, 'Заказ в обработке'),
		(STATUS_READY, 'Заказ готов'),
		(STATUS_COMPLETED, 'Заказ выполнен')
	)

	BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

	customer = models.ForeignKey(Customer, verbose_name='Покупатель',related_name='related_orders', on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255, verbose_name='Имя')
	last_name = models.CharField(max_length=255, verbose_name='Фамилия')
	phone = models.CharField(max_length=20, verbose_name='Телефон')
	cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
	address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
	status = models.CharField(
		max_length=100,
		verbose_name='Статус заказ',
		choices=STATUS_CHOICES,
		default=STATUS_NEW
	)
	buying_type = models.CharField(
		max_length=100,
		verbose_name='Тип заказа',
		choices=BUYING_TYPE_CHOICES,
		default=BUYING_TYPE_SELF
	)
	comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
	created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
	order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)
	
	def __str__(self):
		return str(self.id)



'''
	



	
