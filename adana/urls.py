from django.contrib import admin
from django.urls import path, include

from .settings import MEDIA_URL
from .views import home
from django.conf import settings
from django.conf.urls.static import static
# from adana.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + static(MEDIA_URL, document_root=MEDIA_ROOT)
