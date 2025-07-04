"""
WSGI config for modularSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from django.conf import settings
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modularSystem.settings')

django_app = get_wsgi_application()

application = WhiteNoise(
    django_app,
    root=os.environ.get('STATIC_ROOT', '/app/staticfiles'),
    prefix=os.environ.get('STATIC_URL', '/static/')
)

try:
    from modules.module_discovery import discover_modules
    from engine_module.module_loader import discover_and_register_modules

    discover_modules()
    discover_and_register_modules()
    print("Modules successfully discovered and registered")
except ImportError:
    print("Module discovery skipped - modules not available")
except Exception as e:
    print(f"Module discovery error: {str(e)}")