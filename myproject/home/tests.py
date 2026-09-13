from django.contrib.auth.models import User
from django.test import TestCase


class AuthenticationTests(TestCase):
	def test_register_creates_and_logs_in_user(self):
		response = self.client.post('/register/', {
			'email': 'customer@example.com',
			'password': 'strong-password-123',
			'password_confirmation': 'strong-password-123',
		})

		self.assertRedirects(response, '/')
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		self.assertTrue(User.objects.filter(username='customer@example.com').exists())

	def test_register_rejects_mismatched_passwords(self):
		response = self.client.post('/register/', {
			'email': 'customer@example.com',
			'password': 'strong-password-123',
			'password_confirmation': 'different-password',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Passwords do not match.')
		self.assertFalse(User.objects.exists())

	def test_signin_and_signout(self):
		User.objects.create_user(username='customer@example.com', email='customer@example.com', password='strong-password-123')

		response = self.client.post('/signin/', {
			'email': 'customer@example.com',
			'password': 'strong-password-123',
		})
		self.assertRedirects(response, '/')
		self.assertTrue(response.wsgi_request.user.is_authenticated)

		response = self.client.post('/signout/')
		self.assertRedirects(response, '/')
		self.assertFalse(response.wsgi_request.user.is_authenticated)

	def test_cart_requires_authentication(self):
		response = self.client.get('/cart/')

		self.assertRedirects(response, '/signin/?next=/cart/')

# Create your tests here.
