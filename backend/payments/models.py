from django.db import models

class Order(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount
    currency = models.CharField(max_length=3, default="usd")  # Currency
    is_paid = models.BooleanField(default=False)  # Paid or not
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date

    def __str__(self):
        return f"Order {self.id} - {self.amount} {self.currency}"
