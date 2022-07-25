

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
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})



class MinResalutionErrorException():
	pass


class MaxResalutionErrorException():
	pass




class LatestProductsManager:


	@staticmethod
	def get_products_for_main_page(*args, **kwargs):
		products = []
		ct_models = ContentType.objects.filter(model__in=args)
		for ct_model in ct_models:
			model_products = ct_model.model_class()._base_manager.all().order_by('-id')
			products.extend(model_products)
		return products



class LatestProducts:

	objects = LatestProductsManager()


class CategoryManager(models.Manager):

	
	def get_queryset(self):
		return super().get_queryset()


	def get_categories_for_left_sidebar(self):
		models = get_models_for_count()
		qs = list(self.get_queryset().annotate(*models))
		data = [
			dict(name=c.name, url=c.get_absolute_url())
			for c in qs
		]
		return data


class Category_1(models.Model):

	name = models.CharField(max_length=255, verbose_name="имя категории")
	slug = models.SlugField(unique=True)
	objects = CategoryManager()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'slug': self.slug})

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

class Product(models.Model):

	category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
	title = models.CharField(max_length=255, verbose_name="наименование")
	slug = models.SlugField(unique=True)
	image = models.ImageField(verbose_name='Изображение')
	description = models.TextField(verbose_name='описание', null=True)
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
	count_view = models.PositiveIntegerField(default=0, verbose_name='Количество')

	def __str__(self):
		return self.title

	def get_model_name(self):
		return self.__class__.__name__.lower()


class Notebook(Product):
	diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
	display = models.CharField(max_length=255, verbose_name='тип дисплея')
	processor_freq = models.CharField(max_length=255, verbose_name = 'частота процессора')
	ram = models.CharField(max_length=255, verbose_name = 'оперативная память')
	video = models.CharField(max_length=255, verbose_name = 'видеокарта')
	time_without_charge = models.CharField(max_length=255, verbose_name = 'время работы аккумулятора')
	


	def __str__(self):
		return "{} : {}".format(self.category.name, self.title)

	def get_absolute_url(self):
		return get_product_url(self, 'product_detail')
		

	


class Smartphone(Product):
	diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
	display = models.CharField(max_length=255, verbose_name='тип дисплея')
	resolutions = models.CharField(max_length=255, verbose_name='разрешение экрана')
	accum_volume = models.CharField(max_length=255, verbose_name='объем батареи')
	ram = models.CharField(max_length=255, verbose_name = 'оперативная память')
	sd = models.BooleanField(default=True, verbose_name = 'наличие SD')
	sd_volume = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Максимальный объем SD карты')
	main_cam_mp = models.CharField(max_length=255, verbose_name = 'главная камера')
	frontal_cam_mp = models.CharField(max_length=255, verbose_name = 'фронтальная камера')
	


	def __str__(self):
		return "{} : {}".format(self.category.name, self.title)

	def get_absolute_url(self):
		return get_product_url(self, 'product_detail')

class Lighting(Product):
	name = models.CharField(max_length=255, verbose_name='Наименование товара')
	seria = models.CharField(max_length=255, verbose_name='Серия')
	brand = models.CharField(max_length=255, verbose_name='Брэнд')
	articals = models.CharField(max_length=255, verbose_name='Артикул производителя')
	garant_time = models.CharField(max_length=255, verbose_name='Срок гарантии')
	created_cantry = models.CharField(max_length=255, verbose_name='Страна производитель')
	power = models.CharField(max_length=255, verbose_name='Мощность')
	plinth = models.CharField(max_length=255, verbose_name='Цоколь')
	form_light = models.CharField(max_length=255, verbose_name='Форма Лампы')
	

	

	def __str__(self):
		return "{} : {}".format(self.category.name, self.title)

	def get_absolute_url(self):
		return get_product_url(self, 'product_detail')

class Lampa(Product):
	name = models.CharField(max_length=255, verbose_name='Наименование товара')
	seria = models.CharField(max_length=255, verbose_name='Серия')
	brand = models.CharField(max_length=255, verbose_name='Брэнд')
	articals = models.CharField(max_length=255, verbose_name='Артикул производителя')
	garant_time = models.CharField(max_length=255, verbose_name='Срок гарантии')
	created_cantry = models.CharField(max_length=255, verbose_name='Страна производитель')
	power = models.CharField(max_length=255, verbose_name='Мощность', blank=True)
	plinth = models.CharField(max_length=255, verbose_name='Цоколь')
	form_light = models.CharField(max_length=255, verbose_name='Форма Лампы', blank=True)
	

	def __str__(self):
		return "{} : {}".format(self.category.name, self.title)

	def get_absolute_url(self):
		return get_product_url(self, 'product_detail')

	
class NonStationaryWire(Product):
	name = models.CharField(max_length=255, verbose_name='Наименование товара')
	brand = models.CharField(max_length=255, verbose_name='Брэнд')
	seria = models.CharField(max_length=255, verbose_name='Серия')
	articals = models.CharField(max_length=255, verbose_name='Артикул производителя')
	garant_time = models.CharField(max_length=255, verbose_name='Срок гарантии')
	created_cantry = models.CharField(max_length=255, verbose_name='Страна производитель')
	nominal_section = models.CharField(max_length=255, verbose_name='Наминально сечение проводника')
	material = models.CharField(max_length=255, verbose_name='Материал жил проводника')
	conductor_class = models.CharField(max_length=255, verbose_name='Класс токопроводящей жилы')
	form_wire = models.CharField(max_length=255, verbose_name='Форма жил проводника')
	


	def __str__(self):
		return "{} : {}".format(self.category.name, self.title)

	def get_absolute_url(self):
		return get_product_url(self, 'product_detail')




class CartProduct(models.Model):

	user = models.ForeignKey('Customer', null=True, verbose_name='Покупатель', on_delete=models.CASCADE)
	cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name="related_products")
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	qty = models.PositiveIntegerField(default=1)
	final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая Цена')

	def __str__(self):
		return "Продукт: {} (для корзины)".format(self.content_object.title)

	def save(self, *args, **kwargs):
		self.final_price = self.qty * self.content_object.price
		super().save(*args, **kwargs)

	def get_model_name(self, *args, **kwargs):
		return self.__class__._meta.model_name





class Cart(models.Model):

	owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
	product = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
	total_product = models.PositiveIntegerField(default=0)
	final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая Цена')
	in_order = models.BooleanField(default=False)
	for_anonymous_user = models.BooleanField(default=False)
	


	def __str__(self):
		return str(self.id)

	



 
class Customer(models.Model):


	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
	phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
	address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
	orders = models.ManyToManyField('Order', verbose_name='Заказы полкупателя', related_name='related_customer', blank=True)


	def __str__(self):
		return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


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



class News(models.Model): #модель для написания постов на главное странице
	title = models.CharField(max_length=255, verbose_name='Наименование новости')
	image = models.ImageField(verbose_name='Изображение')
	description = models.TextField(verbose_name='текст новости', null=True)
	
	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'


	



	