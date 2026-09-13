from django.contrib import admin
from .models import Order, OrderItem

admin.site.site_header = 'Noodle Shop Administration'
admin.site.site_title = 'Noodle Shop Admin'
admin.site.index_title = 'Order Management Dashboard'


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ('product_id', 'name', 'price', 'quantity', 'noodle', 'egg')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'payment_method', 'status', 'total', 'created_at')
	list_filter = ('status', 'payment_method', 'created_at')
	search_fields = ('user__email', 'user__username')
	readonly_fields = ('user', 'payment_method', 'subtotal', 'vat', 'total', 'created_at')
	inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'order', 'quantity', 'price', 'egg')
	search_fields = ('name', 'order__user__email')
