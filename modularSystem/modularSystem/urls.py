"""
URL configuration for modularSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.http import JsonResponse
from engine_module.models import InstalledModule as Module
# from modularSystem.engine_module.urls import app_name

def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'message': "Health check successful",
        'services': {
            'database': 'connected',
            'cache': 'active'
        }
    })
urlpatterns = [
    path('', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('modules/', include('engine_module.urls')),
]

for mod in Module.objects.filter(is_active=True):
    try:
        urlpatterns.append(
            path(f"{mod.name}/", include(f"modules.{mod.name}.urls"))
        )
    except ModuleNotFoundError as e:
        print(f"⚠ Modul 'modules.{mod.name}' tidak ditemukan.")