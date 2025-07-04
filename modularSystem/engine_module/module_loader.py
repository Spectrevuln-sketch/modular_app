import os
import importlib
import sys
import time
from django.conf import settings
from django.db import connection, OperationalError, DatabaseError
from django.db.utils import ConnectionHandler
from engine_module.models import InstalledModule

# Flag untuk mencegah eksekusi berulang
DISCOVERY_DONE = False

def discover_and_register_modules():
    global DISCOVERY_DONE
    if DISCOVERY_DONE:
        return

    DISCOVERY_DONE = True

    if 'collectstatic' in sys.argv:
        print("Skipping module discovery during collectstatic")
        return

    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            connection.ensure_connection()

            if 'engine_module_installedmodule' not in connection.introspection.table_names():
                print("Database tables not available. Skipping module discovery.")
                return

            break
        except (OperationalError, DatabaseError) as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt+1}/{max_retries}). Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Database connection failed after multiple attempts. Skipping module discovery.")
                return
        except Exception as e:
            print(f"Unexpected database error: {str(e)}. Skipping module discovery.")
            return

    modules_dir = os.path.join(settings.BASE_DIR, 'modules')
    current_module_names = set()

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if (
            os.path.isdir(module_path) and
            os.path.exists(os.path.join(module_path, 'apps.py'))
        ):
            full_module_path = f'modules.{module_name}'

            _, created = InstalledModule.objects.get_or_create(
                name=module_name,
                defaults={'is_active': True}
            )
            current_module_names.add(module_name)

            if created:
                try:
                    importlib.import_module(full_module_path)
                    print(f"Successfully imported module: {module_name}")
                except ModuleNotFoundError as e:
                    print(f"Failed to import module {module_name}: {e}")
                    continue

    installed_names = set(InstalledModule.objects.values_list('name', flat=True))
    removed_modules = installed_names - current_module_names
    if removed_modules:
        print(f"Removing deleted modules: {', '.join(removed_modules)}")
        InstalledModule.objects.filter(name__in=removed_modules).delete()