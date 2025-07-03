import os
from django.apps import AppConfig
from django.conf import settings
class EngineModularConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engine_module'
    verbose_name = 'Modular Engine'



    def ready(self):
       from modules.module_discovery import discover_modules
       discover_modules()
       from .module_loader import discover_and_register_modules
       discover_and_register_modules()