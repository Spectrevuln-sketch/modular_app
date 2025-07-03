from django.urls import path
from . import views

app_name = 'product_module'

urlpatterns = [
    path('',        views.product_list,   name='product-list'),
    path('create/', views.product_create, name='product-create'),
    path('delete/<int:pk>/', views.product_delete, name='product-delete'),
    path('update/<int:pk>/', views.product_update, name='product-update'),
]