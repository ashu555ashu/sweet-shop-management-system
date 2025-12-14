from django.contrib import admin
from .models import Sweet

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ('sweet_id', 'name', 'price', 'category', 'quantity')
