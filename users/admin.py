from django.contrib import admin

# Register your models here.
from .models import CustomerUser,Product,Order,OrderItem
admin.site.register(CustomerUser)
admin.site.register(Product)

admin.site.register(Order)
admin.site.register(OrderItem)