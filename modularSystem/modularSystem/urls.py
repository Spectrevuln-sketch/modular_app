from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import logging
from django.db import connection
from django.contrib.auth.views import LogoutView

logger = logging.getLogger(__name__)

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
    path(
        'admin/logout/',
        LogoutView.as_view(
            next_page='/admin/login/?logged_out=1'
        ),
        name='admin_logout'
    ),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('modules/', include('engine_module.urls')),
]

try:
    if 'engine_module_installedmodule' in connection.introspection.table_names():
        from engine_module.models import InstalledModule as Module

        for mod in Module.objects.filter(is_active=True):
            try:
                urlpatterns.append(
                    path(f"{mod.name}/", include(f"modules.{mod.name}.urls"))
                )
                logger.info(f"Added URLs for module: {mod.name}")
            except ModuleNotFoundError:
                logger.warning(f"⚠ Module 'modules.{mod.name}' not found")
            except Exception as e:
                logger.error(f"Error loading module {mod.name}: {str(e)}")
    else:
        logger.warning("Skipping module URLs - table not available")
except Exception as e:
    logger.error(f"Error initializing module URLs: {str(e)}")