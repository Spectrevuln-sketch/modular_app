from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
import django.views.decorators.http
from .models import Product
from .forms import ProductForm
from engine_module.models import InstalledModule as Module

@permission_required('product_module.view_product', raise_exception=True)
def product_list(request):
    # Module check
    app_label = request.resolver_match.app_name
    print(f"App label: {app_label}")

    if not Module.objects.filter(name=app_label, is_active=True).exists():
        raise Http404("Module not installed")

    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@permission_required('product_module.add_product', raise_exception=True)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_module:product-list')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {
        'form': form,
        'title': "Create New Product",
        'object': None
    })

@permission_required('product_module.change_product', raise_exception=True)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_module:product-list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {
        'form': form,
        'title': "Update Product",
        'object': product
    })

@require_POST
@permission_required('product_module.delete_product', raise_exception=True)
def product_delete(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return JsonResponse({'success': True})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)