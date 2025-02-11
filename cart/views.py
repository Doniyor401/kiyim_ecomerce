from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.db.models import Count


def cart(request, total = 0, tax=0, gen_total=0, cart_items=None):

    try:
        cart = Cart.objects.get(session_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.quantity*cart_item.product.price
        tax = (total * 2) / 100
        gen_total = total - tax
    except ObjectDoesNotExist:
        pass
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'gen_total': gen_total
    }
    return render(request, 'cart.html', context)
    
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required
def add_cart(request, product_id):
    # variations obyektlarini xosil qilish
    variations = []
    data = dict(request.POST)
    data.pop('csrfmiddlewaretoken')
    for category, value in data.items():
        var = Variation.objects.get(category=category, value=value[0])
        variations.append(var)

    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))      
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_id=_cart_id(request))
    cart.save()
    
    try:
        cart_item = CartItem.objects.filter(product=product, cart=cart, variations__in = variations).annotate(num = Count('variations')).get(num=len(variations))
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.variations.set(variations)
        cart_item.save()
    return redirect('cart')


def sub_cart(request, item_id):

    cart_item = CartItem.objects.get(pk=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def cart_increment(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def remove_cart(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.delete()
    return redirect('cart')