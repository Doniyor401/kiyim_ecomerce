from django.urls import path
from .views import *

urlpatterns = [
    path('', store, name="store"),
    path('search/', search, name='search'),
    path('<slug:category_slug>/', store, name="products_by_category"),
    path('<slug:category_slug>/<slug:product_slug>', product_detail, name="product_detail"),

]
