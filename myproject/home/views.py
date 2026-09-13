from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme


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
    return render(request, 'home/bill.html')


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