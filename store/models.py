from django.db import models
from django.contrib.auth.models import User
from django.conf.urls.static import static
# Create your models here.


class CustomerModel(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return "{}. {}".format(self.id, self.name)


class TagModel(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    tag = models.ManyToManyField(TagModel, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        default='placeholder.jpg', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/images/placeholder.jpg'
        return url


class OrderModel(models.Model):
    customer = models.ForeignKey(
        CustomerModel, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitemmodel_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def getCartTotal(self):
        order_items = self.orderitemmodel_set.all()
        total = sum([item.getTotal for item in order_items])
        return total

    @property
    def getCartItems(self):
        order_items = self.orderitemmodel_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItemModel(models.Model):
    product = models.ForeignKey(
        ProductModel, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddressModel(models.Model):
    customer = models.ForeignKey(
        CustomerModel, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
