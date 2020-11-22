from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CustomerModel)
admin.site.register(ProductModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
admin.site.register(ShippingAddressModel)
admin.site.register(TagModel)
