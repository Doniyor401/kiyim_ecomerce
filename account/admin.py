from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')  #admin panelga qaysi fieldlar chiqishi
    list_display_links = ('email', 'first_name', 'last_name')   #email,firstname,lastname bosganda ichiga o'tadi
    ordering = ('-date_joined',)   # qaysi field bo'yicha chiqishi
    # exclude = ('password', )   #passwordni admin panelga chiqarmaslik uchun

    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff')  #filter qilish yon tarafidan
    fieldsets = (
        (None, {
            'fields': ('avatar', 'email', 'username', 'user_company', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin'),
            'classes': ('collapse',)  # bekitish imkoniyati qo'shadi
        }),
    )    #user ichiga kirganda qaysi fieldar chiqishi
