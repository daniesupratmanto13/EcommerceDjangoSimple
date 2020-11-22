import json


from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {
        'getCartTotal': 0,
        'getCartItems': 0,
        'shipping': False,
    }
    cart_items = order['getCartItems']
    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product = ProductModel.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['getCartTotal'] += total
            order['getCartItems'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'tag': product.tag,
                    'description': product.description,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'getTotal': total,
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }


def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitemmodel_set.all()
        cart_items = order.getCartItems
    else:
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']
    return {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }


def guestOrder(request, data):

    name = data['form']['name']
    email = data['form']['email']
    cookie_data = cookieCart(request)
    items = cookie_data['items']

    customer, created = CustomerModel.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = OrderModel.objects.create(customer=customer, complete=False)

    for item in items:
        product = ProductModel.objects.get(id=item['product']['id'])
        order_item = OrderItemModel.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
