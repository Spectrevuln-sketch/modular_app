from django.core.management.base import BaseCommand
from engine_module.module_loader import discover_and_register_modules

class Command(BaseCommand):
    help = 'Initialize application modules'

    def handle(self, *args, **options):
        discover_and_register_modules()
        self.stdout.write(self.style.SUCCESS("Application modules initialized"))