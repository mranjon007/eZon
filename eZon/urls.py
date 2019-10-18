
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ezon_admin/', admin.site.urls),  # this_url_name should be changed in Production
    path('order/', include('order_management.urls')),
    path('', RedirectView.as_view(url='/order/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('user.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
