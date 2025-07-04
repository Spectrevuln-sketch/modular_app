import os
import importlib
import sys
from django.conf import settings
from django.db import connection, OperationalError
from engine_module.models import InstalledModule

def discover_modules():
    if 'collectstatic' in sys.argv:
        return

    modules_dir = os.path.join(settings.BASE_DIR, 'modules')

    try:
        if not connection.introspection.table_names():
            return

        for module_name in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, module_name)
            if (
                os.path.isdir(module_path)
                and os.path.exists(os.path.join(module_path, 'apps.py'))
                and module_name not in settings.INSTALLED_APPS
            ):
                InstalledModule.objects.get_or_create(
                    name=module_name,
                    defaults={'is_active': False}
                )

                try:
                    importlib.import_module(f'modules.{module_name}')
                except ModuleNotFoundError:
                    continue

    except OperationalError:
        pass