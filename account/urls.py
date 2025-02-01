from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
]
