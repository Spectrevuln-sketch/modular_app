from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.stock is None:
            raise ValidationError({'stock': 'Stock quantity is required.'})

        if self.stock < 0:
            raise ValidationError({'stock': 'Stock cannot be negative.'})

        if self.price is None:
            raise ValidationError({'price': 'Price is required.'})

        if self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative.'})

    def __str__(self):
        return self.name