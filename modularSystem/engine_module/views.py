from django.shortcuts import render, redirect
from .models import InstalledModule
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from importlib import import_module

def module_manager(request):
    installed_modules = InstalledModule.objects.all()

    available_modules = []
    for app in settings.INSTALLED_APPS:
        if app.startswith('modules.'):
            module_name = app.split('.')[-1]
            try:
                mod = import_module(f"{app}.app_config")
                module_config = getattr(mod, 'ModuleConfig', None)
                if module_config:
                    available_modules.append({
                        'name': module_name,
                        'display_name': getattr(module_config, 'verbose_name', module_name),
                        'description': getattr(module_config, 'description', ''),
                    })
            except ImportError:
                continue

    return render(request, 'module_manager.html', {
        'installed_modules': installed_modules,
        'available_modules': available_modules
    })

@require_POST
def toggle_module(request, module_name, action):
    print(f"Toggle module: {module_name}, action: {action}")
    try:
        module = InstalledModule.objects.get(name=module_name)

        if action == 'install' and not module.is_active:
            from django.core.management import call_command
            call_command('migrate', f"{module_name}")
            module.is_active = True
            module.save()
            messages.success(request, f"Module {module_name} installed successfully!")

        elif action == 'uninstall' and module.is_active:
            module.is_active = False
            module.save()
            messages.warning(request, f"Module {module_name} uninstalled!")

        elif action == 'upgrade':
            from django.core.management import call_command
            call_command('makemigrations', f"{module_name}")
            call_command('migrate', f"{module_name}")
            module.version += 1
            module.save()
            messages.info(request, f"Module {module_name} upgraded to v{module.version}!")

    except InstalledModule.DoesNotExist:
        if action == 'install':
            InstalledModule.objects.create(name=module_name, is_active=True)
            messages.success(request, f"Module {module_name} installed successfully!")
        else:
            messages.error(request, f"Module {module_name} not found!")

    return redirect('engine_module:module-manager')
