from django.contrib import admin

from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество пустых форм для добавления изображений


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ('name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'discount', 'image', 'stock', 'is_available', 'category')
        }),
        ('Permissions', {
            'fields': ('slug', ),
            'classes': ('collapse',)  # bekitish imkoniyati qo'shadi
        }),
    )  # user ichiga kirganda qaysi fieldar chiqishi

    # dinamik ravishda fieldlarni ko'rsatish -> korishda check qilib bunisi chiqadi
    def get_fields(self, request, obj=None):
        if obj is None:  # narsa qoshvotkanda (obj == None)
            return ['name', 'description', 'price', 'image', 'stock', 'is_available', 'category']  # xammasi korinadi
        return super().get_fields(request, obj)

    # dinamik ravishda fieldlarni ko'rsatish -> Product qoshvotkanda bunisi chiqadi(add)
    def get_fieldsets(self, request, obj=None):
        if obj is None:  # narsa qoshvotkan (obj == None)
            return [
                (None, {
                    'fields': ('name', 'slug', 'description', 'price', 'image', 'stock', 'is_available', 'category')
                }),
            ]
        return super().get_fieldsets(request, obj)


admin.site.register(ProductImage)
