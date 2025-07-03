import os
import importlib
from django.conf import settings
from engine_module.models import InstalledModule

def discover_modules():
    modules_dir = os.path.join(settings.BASE_DIR, 'modules')

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if (
            os.path.isdir(module_path)
            and os.path.exists(os.path.join(module_path, 'apps.py'))
            and module_name not in settings.INSTALLED_APPS
        ):
            if not InstalledModule.objects.filter(name=module_name).exists():
                InstalledModule.objects.create(name=module_name, is_active=False)

            try:
                importlib.import_module(f'modules.{module_name}')
            except ModuleNotFoundError:
                continue
