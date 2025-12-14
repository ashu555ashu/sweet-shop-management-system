from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Sweet(models.Model):
    sweet_id = models.CharField(max_length=10, unique=True)  # unique ID
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50)  # New field
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='sweet_image/', blank=True, null=True)

    def __str__(self):
        return self.name

