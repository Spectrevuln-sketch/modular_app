from engine_module.models import InstalledModule

def active_modules(request):
    return {
        'active_modules': InstalledModule.objects.filter(is_active=True)
    }
