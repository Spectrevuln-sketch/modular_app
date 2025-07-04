import sys
from django.apps import AppConfig

class EngineModularConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engine_module'
    verbose_name = 'Modular Engine'

    def ready(self):
        runtime_commands = ['runserver', 'uwsgi', 'gunicorn']

        if any(cmd in sys.argv for cmd in runtime_commands):
            print("Initializing module discovery...")
            try:
                from .module_loader import discover_and_register_modules
                discover_and_register_modules()
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Module initialization error: {str(e)}")