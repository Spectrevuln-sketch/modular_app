from django.db import models

class InstalledModule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} v{self.version}"