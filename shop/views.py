from django.shortcuts import render
from sweets.models import Sweet
from django.contrib.auth.decorators import login_required

@login_required
def shop_home(request):
    sweets = Sweet.objects.all()
    return render(request, 'shop.html', {'sweets': sweets})

@login_required
def my_shop(request):
    return render(request, 'myshop.html')