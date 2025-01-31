from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = ()
    list_filter = ('name',)  # yon tarafda name boyicha filter qiladi

    # Korvotkanda qaysi fieldlarni ko'rsatish
    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        ('Mayda chuda', {
            'fields': ('description', 'image'),
            'classes': ('collapse',)  # Razdelli bekitish imkoniyatini beradi
        }),
    )

    # dinamik ravishda fieldlarni ko'rsatish -> korishda check qilib bunisi chiqadi
    def get_fields(self, request, obj=None):
        if obj is None:  # narsa qoshvotkanda (obj == None)
            return ['name', 'slug', 'description', 'image']  # xammasi korinadi
        return super().get_fields(request, obj)

    # dinamik ravishda fieldlarni ko'rsatish -> Category qoshvotkanda bunisi chiqadi(add)
    def get_fieldsets(self, request, obj=None):
        if obj is None:  # narsa qoshvotkan (obj == None)
            return [
                (None, {
                    'fields': ('name', 'slug', 'description', 'image')
                }),
            ]
        return super().get_fieldsets(request, obj)
