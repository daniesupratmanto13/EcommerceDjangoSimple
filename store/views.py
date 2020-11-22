# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.http import request
import datetime
import json

# Create your views here.
from .models import *
from .utils import *


def indexStoreView(request):

    # cartData function from .utils return dict {items, order, cart_items} from model or cookies
    data = cartData(request)
    cart_items = data['cart_items']
    product = ProductModel.objects.all()
    context = {
        'products': product,
        'cart_items': cart_items,
    }
    return render(request, 'store/index.html', context)


def cartView(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


def checkoutView(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):

    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    customer = request.user.customermodel
    product = ProductModel.objects.get(id=product_id)
    order, created = OrderModel.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItemModel.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


# @csrf_exempt
def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(
            customer=customer, complete=False)

    else:
        # guestOrder fuction from .utils return customer and order from cookies
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.getCartTotal):
        order.complete = True
        order.save()

    if order.shipping == True:
        ShippingAddressModel.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
        )

    return JsonResponse('Pyment Complete', safe=False)
