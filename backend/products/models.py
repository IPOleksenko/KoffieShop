from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price", validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    image = models.URLField(blank=True, default=settings.DEFAULT_PRODUCT_IMAGE, verbose_name="Image URL")  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    stripe_product_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        editable=False,
        verbose_name="Stripe Product ID"
    )
    stripe_price_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        editable=False,
        verbose_name="Stripe Price ID"
    )
    def __str__(self):
        return self.name
