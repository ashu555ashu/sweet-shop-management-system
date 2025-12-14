from django.db import models
from django.conf import settings
from sweets.models import Sweet

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    sweet = models.ForeignKey(
        Sweet,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'sweet')

    @property
    def subtotal(self):
        return self.quantity * self.sweet.price

    def __str__(self):
        return f"{self.quantity} x {self.sweet.name}"
