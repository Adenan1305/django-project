from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from decimal import Decimal, ROUND_HALF_UP

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Order, OrderItem


PRODUCT_CATALOG = {
    1: ('Tom Yum Noodles + rice', Decimal('70.00')),
    2: ('Beef offal rice with spicy dipping sauce', Decimal('80.00')),
    3: ('Beef noodles + Chicken noodles', Decimal('100.00')),
    4: ('Tom Yum Noodles', Decimal('65.00')),
    5: ('Chicken noodles', Decimal('50.00')),
    6: ('Beef noodles', Decimal('65.00')),
    7: ('Bottled Water', Decimal('15.00')),
    8: ('Soft Drinks', Decimal('25.00')),
    9: ('Ice cream', Decimal('30.00')),
    10: ('Beef intestines with spicy dipping sauce', Decimal('50.00')),
    11: ('Fried meatballs', Decimal('30.00')),
    12: ('Fried dumplings', Decimal('15.00')),
}


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'home/index.html')


def menu(request):
    """Display the shop menu."""
    return render(request, 'home/menu.html')


@login_required
def cart(request):
    """Display the current shopping cart."""
    return render(request, 'home/cart.html')


@login_required
def bill(request):
    """Display the receipt for the most recent order."""
    order_id = request.GET.get('order')
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        pk=order_id,
        user=request.user,
    ) if order_id else Order.objects.prefetch_related('items').filter(user=request.user).first()
    if order is None:
        return redirect('portfolio:menu')
    return render(request, 'home/bill.html', {'order': order})


def service(request):
    """Display the shop services and customer information."""
    return render(request, 'home/service.html')


def signin(request):
    """Sign a customer in with the email used during registration."""
    if request.user.is_authenticated:
        return redirect('portfolio:index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '')
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('portfolio:index')
        messages.error(request, 'Email or password is incorrect.')

    return render(request, 'home/signin.html', {'next': request.GET.get('next', '')})


def register(request):
    """Create a customer account and sign the customer in."""
    if request.user.is_authenticated:
        return redirect('portfolio:index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password_confirmation = request.POST.get('password_confirmation', '')

        if not email or not password:
            messages.error(request, 'Please complete all required fields.')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'This email is already registered.')
        elif password != password_confirmation:
            messages.error(request, 'Passwords do not match.')
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            return redirect('portfolio:index')

    return render(request, 'home/register.html')


def signout(request):
    """End the current customer session."""
    if request.method == 'POST':
        logout(request)
    return redirect('portfolio:index')


@login_required
def create_order(request):
    """Persist a checkout order submitted by the authenticated customer."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required.'}, status=405)

    try:
        payload = json.loads(request.body)
        payment_method = payload.get('payment')
        cart = payload.get('cart', [])
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid order data.'}, status=400)

    if payment_method not in dict(Order.PAYMENT_METHODS) or not isinstance(cart, list) or not cart:
        return JsonResponse({'error': 'A valid payment method and cart are required.'}, status=400)

    subtotal = Decimal('0.00')
    items = []
    for item in cart:
        try:
            product_id = int(item['id'])
            quantity = int(item['qty'])
            name, price = PRODUCT_CATALOG[product_id]
            if quantity < 1:
                raise ValueError
        except (KeyError, TypeError, ValueError, ArithmeticError):
            return JsonResponse({'error': 'Invalid cart item.'}, status=400)

        egg = bool(item.get('egg'))
        item_price = price + (Decimal('10.00') if egg else Decimal('0.00'))
        subtotal += item_price * quantity
        items.append({
            'product_id': product_id,
            'name': name,
            'price': item_price,
            'quantity': quantity,
            'noodle': str(item.get('noodle', ''))[:50],
            'egg': egg,
        })

    subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    vat = (subtotal * Decimal('0.07')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    order = Order.objects.create(
        user=request.user,
        payment_method=payment_method,
        subtotal=subtotal,
        vat=vat,
        total=subtotal + vat,
    )
    OrderItem.objects.bulk_create([OrderItem(order=order, **item) for item in items])
    return JsonResponse({'redirect_url': f'/bill/?order={order.pk}'}, status=201)