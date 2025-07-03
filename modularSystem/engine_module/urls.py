from django.urls import path
from . import views

app_name = 'engine_module'
urlpatterns = [
    path('', views.module_manager, name='module-manager'),
    path('<str:module_name>/<str:action>/', views.toggle_module, name='toggle-module'),
]