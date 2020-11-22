from django.urls import path

from .views import *

app_name = 'store'

urlpatterns = [
    path('cart/', cartView, name='cart'),
    path('checkout/', checkoutView, name='checkout'),
    path('', indexStoreView, name='index'),

    path('update_item/', updateItem, name='update_item'),
    path('process_order/', processOrder, name='process_order'),
]
