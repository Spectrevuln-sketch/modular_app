import os
import importlib
from django.conf import settings
from engine_module.models import InstalledModule
from django.core.management import call_command

def discover_and_register_modules():
    modules_dir = os.path.join(settings.BASE_DIR, 'modules')
    current_module_names = set()

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if (
            os.path.isdir(module_path)
            and os.path.exists(os.path.join(module_path, 'apps.py'))
        ):
            full_module_path = f'modules.{module_name}'

            InstalledModule.objects.get_or_create(name=module_name, defaults={'is_active': True})
            current_module_names.add(module_name)

            try:
                importlib.import_module(full_module_path)
            except ModuleNotFoundError:
                continue

    installed_names = set(InstalledModule.objects.values_list('name', flat=True))
    removed_modules = installed_names - current_module_names
    if removed_modules:
        InstalledModule.objects.filter(name__in=removed_modules).delete()
    call_command("migrate", interactive=False)
