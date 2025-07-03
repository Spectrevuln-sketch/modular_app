from django.apps import AppConfig

class ProductModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.product_module'
    verbose_name = 'Product Management Module'

    def ready(self):
        try:
            from . import permissions
            permissions.setup_permissions()
        except ImportError:
            pass