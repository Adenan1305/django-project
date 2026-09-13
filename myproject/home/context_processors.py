from django.contrib.auth.models import User

from .models import Order


def admin_dashboard(request):
    if not request.path.startswith('/admin/'):
        return {}

    return {
        'dashboard_order_count': Order.objects.count(),
        'dashboard_customer_count': User.objects.filter(is_superuser=False).count(),
        'dashboard_menu_count': 12,
        'dashboard_revenue': sum((order.total for order in Order.objects.all()), 0),
        'dashboard_recent_orders': Order.objects.select_related('user').prefetch_related('items')[:5],
    }