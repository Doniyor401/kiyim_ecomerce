from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
from cart.models import CartItem
from category.models import Category
from .models import Product
from cart.views import _cart_id
from django.core.paginator import Paginator


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
    if keyword:
        products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))

    context = {
        'products': products,
        'product_count': products.count()
    }
    return render(request, 'store.html', context)


# def store(request, category_slug=None):
#     if category_slug is None:
#         products = Product.objects.filter(is_available=True).order_by('id')
#     else:
#         categories = get_object_or_404(Category, slug=category_slug)
#         products = Product.objects.filter(is_available=True, category=categories).order_by('id')
#
#     paginator = Paginator(products, 1)
#     page = request.GET.get('page')
#     paged_products = paginator.get_page(page)
#
#
#     context = {
#         'products': paged_products,
#         'product_count': products.count()
#     }
#     return render(request, 'store.html', context)

def store(request, category_slug=None):
    # Получаем список товаров в зависимости от категории
    if category_slug is None:
        products = Product.objects.filter(is_available=True).order_by('id')
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=category).order_by('id')

    # Пагинация: по 10 товаров на страницу
    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # Логика для отображения только нужных страниц и многоточий
    page_range = paginator.page_range
    displayed_pages = []

    for num in page_range:
        if num <= 3 or num > paginator.num_pages - 3 or (
                num >= paged_products.number - 2 and num <= paged_products.number + 2):
            displayed_pages.append(num)
        elif num == 4 or num == paginator.num_pages - 3:
            displayed_pages.append("...")

    # Передаем данные в контекст
    context = {
        'products': paged_products,
        'product_count': products.count(),
        'displayed_pages': displayed_pages,  # Передаем страницы с многоточием
        'category_slug': category_slug,  # Слаг категории, если есть
    }

    return render(request, 'store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    cart_in = CartItem.objects.filter(cart__session_id=_cart_id(request), product=product).exists()  # Check if product is in cart
    context = {
        'product': product,
        'cart_in': cart_in
    }
    return render(request, 'product_detail.html', context)
