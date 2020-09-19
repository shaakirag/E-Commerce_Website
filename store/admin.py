from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Favourite)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
