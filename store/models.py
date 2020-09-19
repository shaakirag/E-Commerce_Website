from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	is_user = models.BooleanField(default=False, null=True, blank=True)
	email = models.EmailField(max_length=254)
	phone = models.CharField(max_length=500, null=True)
	profile_pic = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.first_name

	@property
	def imageURL(self):
		try:
			url = self.profile_pic.url
		except:
			url = '/static/images/avatar-placeholder.png'
		print('URL:', url)
		return url

class Category(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	featured = models.ImageField(null=True)
	price = models.DecimalField(max_digits=100, decimal_places=2,null=True)
	digital = models.BooleanField(default=False,null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="category")
	tag = models.ManyToManyField(Tag, blank=True, related_name="tags")
	in_cart = models.BooleanField(default=False,null=True, blank=True)
	in_fav = models.BooleanField(default=False,null=True, blank=True)


	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.featured.url
		except:
			url = ''
		print('URL:', url)
		return url
	
	@property
	def get_product_quantity(self):
		orderitems = self.orderitem_set.filter(product=self.id)
		total = sum([item.quantity for item in orderitems])
		return total	


class Image(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField()

	def __str__(self):
		return self.product.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		print('URL:', url)
		return url

class Favourite(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.user.username

class Review(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rating = models.IntegerField()
	text = models.TextField(max_length=500)

	def __str__(self):
		return '{}-{}'.format(self.product.name, str(self.user.username))

class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
		
	@property
	def get_orderItems(self):
		orderitems = self.orderitem_set.all()
		return orderitems 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.name

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	country = models.CharField(max_length=200, null=False)
	province = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=False)
	address = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address