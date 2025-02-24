from django.db import models

class Order(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="usd")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    items = models.JSONField()

    def __str__(self):
        return f"Order {self.id} - {self.amount} {self.currency}"