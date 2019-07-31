"""eZon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
