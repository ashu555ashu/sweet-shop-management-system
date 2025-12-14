from django.shortcuts import render, redirect, get_object_or_404
from sweets.models import Sweet

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for sweet_id, qty in cart.items():
        sweet = get_object_or_404(Sweet, id=sweet_id)
        cart_items.append({
            'sweet': sweet,
            'quantity': qty,
            'subtotal': sweet.price * qty
        })
        total += sweet.price * qty

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, sweet_id):
    cart = request.session.get('cart', {})
    sweet = get_object_or_404(Sweet, id=sweet_id)

    if cart.get(str(sweet_id), 0) < sweet.quantity:
        cart[str(sweet_id)] = cart.get(str(sweet_id), 0) + 1
        request.session['cart'] = cart

    return redirect('cart:cart_view')

def remove_from_cart(request, sweet_id):
    cart = request.session.get('cart', {})
    if str(sweet_id) in cart:
        del cart[str(sweet_id)]
        request.session['cart'] = cart
    return redirect('cart:cart_view')

def checkout(request):
    # optional: clear cart & create order
    request.session['cart'] = {}
    return render(request, 'cart/checkout.html')
