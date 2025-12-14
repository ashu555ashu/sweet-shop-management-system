from django.db import models
from django.conf import settings
from sweets.models import Sweet
from datetime import timedelta
from django.utils import timezone

class Order(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Card Payment'),
        ('UPI', 'UPI Payment'),
        ('NETBANK', 'Net Banking'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=timezone.now() + timedelta(days=3))
    shipping_address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    sweet = models.ForeignKey(
        Sweet,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.sweet.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.sweet.name}"
