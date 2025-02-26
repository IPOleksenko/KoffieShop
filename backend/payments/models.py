from django.db import models

ORDER_STATUS_CHOICES = [
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('completed', 'Completed'),
]

class Recipient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name="orders")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="usd")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    items = models.JSONField()  # Contains product data
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Order {self.id} - {self.amount} {self.currency} - {self.get_status_display()}"
