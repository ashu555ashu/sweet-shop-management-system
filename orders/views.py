from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from sweet.models import Sweet
from .models import Order, OrderItem
from cart.utils import get_cart_items  # utility to get cart items

@login_required
def place_order(request):
    cart_items = get_cart_items(request.user)
    if not cart_items:
        return redirect('cart:view_cart')

    total = sum(item.sweet.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            sweet=item.sweet,
            quantity=item.quantity,
            price=item.sweet.price
        )
        # Decrease sweet stock
        item.sweet.quantity -= item.quantity
        item.sweet.save()

    # Clear user cart
    clear_cart(request.user)

    return redirect('order:order_success', order_id=order.id)
