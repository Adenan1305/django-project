from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
	PAYMENT_METHODS = (
		('PromptPay', 'PromptPay'),
		('Cash', 'Cash'),
	)
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('preparing', 'Preparing'),
		('completed', 'Completed'),
		('cancelled', 'Cancelled'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	subtotal = models.DecimalField(max_digits=10, decimal_places=2)
	vat = models.DecimalField(max_digits=10, decimal_places=2)
	total = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f'Order #{self.pk} - {self.user.email}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product_id = models.PositiveIntegerField()
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField()
	noodle = models.CharField(max_length=50, blank=True)
	egg = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name} x{self.quantity}'
