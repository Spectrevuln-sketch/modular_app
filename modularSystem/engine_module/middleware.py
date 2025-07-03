from django.http import Http404
from .models import InstalledModule

class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/products/'):
            try:
                module = InstalledModule.objects.get(name='product_module')
                if not module.is_active:
                    raise Http404("Module is not active")
            except InstalledModule.DoesNotExist:
                raise Http404("Module not installed")