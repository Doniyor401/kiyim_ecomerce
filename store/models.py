from django.db import models
from django.urls import reverse
from category.models import Category
from django.core.exceptions import ValidationError
from django.utils import timezone
from account.models import Account


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image = models.ImageField(upload_to = 'photoes/products')
    # ombordagi soni
    stock = models.IntegerField(default=1)
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    # bu metodni qoshmasak xato ekranga kotta bob chiqadi
    def clean(self):
        if self.stock < 0:
            raise ValidationError({'stock': 'Axmoq qanaqa qib minus bolishi mumkun? 😂 Xotyabi 0 qib qoy'})
        if self.stock <= 0:
            self.is_available = True  # Agar tovar nalichida bomasa is_available ni False qb qoyadi
        else:
            self.is_available = True  # Agar tovar nalichida bosa is_available ni True qiladi


    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.is_available = False  # Agar tovar nalichida bomasa is_available ni False qb qoyadi
        else:
            self.is_available = True  # Agar tovar nalichida bosa is_available ni True qiladi

        self.clean()
        super().save(*args, **kwargs)  # Original save metodini chaqirib saqlab qoyish uchun


    def get_price_with_discount(self):
        if self.discount > 0:
            return round(self.price * (1 - (self.discount / 100)), 2)
        return round(self.price, 2)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photoes/products', blank=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)  # Описание изображения (опционально)

    def __str__(self):
        return f"Image for {self.product.name}"

