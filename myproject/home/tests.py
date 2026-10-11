import json
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Order, UserPoints


class AuthenticationTests(TestCase):
	def test_register_creates_and_logs_in_user(self):
		response = self.client.post('/register/', {
			'email': 'customer@example.com',
			'password': 'strong-password-123',
			'password_confirmation': 'strong-password-123',
		})

		self.assertRedirects(response, '/')
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		user = User.objects.get(username='customer@example.com')
		self.assertEqual(user.points.points, 0)

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
		user = User.objects.create_user(username='customer@example.com', email='customer@example.com', password='strong-password-123')
		UserPoints.objects.create(user=user, points=25)

		response = self.client.post('/signin/', {
			'email': 'customer@example.com',
			'password': 'strong-password-123',
		})
		self.assertRedirects(response, '/')
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		self.assertEqual(self.client.get('/api/points/').json(), {'points': 25})

		response = self.client.post('/signout/')
		self.assertRedirects(response, '/')
		self.assertFalse(response.wsgi_request.user.is_authenticated)
		points_response = self.client.get('/api/points/')
		self.assertEqual(points_response.status_code, 302)

	def test_guest_can_open_cart(self):
		response = self.client.get('/cart/')

		self.assertEqual(response.status_code, 200)

	def test_points_are_only_shown_to_authenticated_users(self):
		guest_response = self.client.get('/')
		self.assertNotContains(guest_response, 'id="user-points"')

		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		UserPoints.objects.create(user=user)
		self.client.force_login(user)
		authenticated_response = self.client.get('/')
		self.assertContains(authenticated_response, 'id="user-points"')
		self.assertContains(authenticated_response, 'id="points-value">0</span>')
		self.assertContains(authenticated_response, 'href="/menu/#rewards-section"')

	def test_rewards_are_only_redeemable_from_menu_when_authenticated(self):
		guest_response = self.client.get('/menu/')
		self.assertEqual(guest_response.status_code, 200)
		self.assertContains(guest_response, 'Sign in to earn and redeem reward points.')
		self.assertNotContains(guest_response, 'onclick="redeemReward(9)"')

		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		self.client.force_login(user)

		authenticated_response = self.client.get('/menu/')
		self.assertContains(authenticated_response, 'id="rewards-points-value"')
		self.assertContains(authenticated_response, '<details id="rewards-section"')
		self.assertNotContains(authenticated_response, '<details id="rewards-section" open')
		self.assertContains(authenticated_response, 'onclick="redeemReward(9)"')
		self.assertContains(authenticated_response, 'onclick="redeemReward(11)"')
		self.assertContains(authenticated_response, 'home/js/rewards.js')

	def test_admin_dashboard_and_standard_admin_pages_use_custom_styles(self):
		admin_user = User.objects.create_superuser(
			username='admin@example.com',
			email='admin@example.com',
			password='strong-password-123',
		)
		self.client.force_login(admin_user)

		dashboard_response = self.client.get('/admin/')
		self.assertEqual(dashboard_response.status_code, 200)
		self.assertContains(dashboard_response, 'home/css/admin-pages.css?v=9')
		self.assertContains(dashboard_response, 'home/css/admin.css?v=8')
		self.assertContains(dashboard_response, 'class="ns-orders-card"')
		self.assertContains(dashboard_response, 'href="/admin/home/order/"')
		self.assertContains(dashboard_response, 'href="/admin/auth/user/"')
		self.assertContains(dashboard_response, 'href="/admin/home/orderitem/"')

		home_app_response = self.client.get('/admin/home/')
		self.assertRedirects(home_app_response, '/admin/')

		order_list_response = self.client.get('/admin/home/order/')
		self.assertEqual(order_list_response.status_code, 200)
		self.assertContains(order_list_response, 'home/css/admin-pages.css?v=9')
		self.assertNotContains(order_list_response, 'home/css/admin.css?v=8')
		self.assertContains(order_list_response, '>Noodle Shop</a>')
		self.assertNotContains(order_list_response, '>Home</a>\n› <a href="/admin/home/')

		order_items_response = self.client.get('/admin/home/orderitem/')
		self.assertEqual(order_items_response.status_code, 200)
		self.assertContains(order_items_response, 'home/css/admin-pages.css?v=9')

		user_change_response = self.client.get(f'/admin/auth/user/{admin_user.pk}/change/')
		self.assertEqual(user_change_response.status_code, 200)
		self.assertContains(user_change_response, 'home/css/admin-pages.css?v=9')

		order = Order.objects.create(
			user=admin_user,
			payment_method='Cash',
			subtotal=Decimal('10.00'),
			vat=Decimal('0.70'),
			total=Decimal('10.70'),
		)
		order_change_response = self.client.get(f'/admin/home/order/{order.pk}/change/')
		self.assertEqual(order_change_response.status_code, 200)
		self.assertContains(order_change_response, 'home/css/admin-pages.css?v=9')

		order_add_response = self.client.get('/admin/home/order/add/')
		self.assertEqual(order_add_response.status_code, 200)
		self.assertContains(order_add_response, 'home/css/admin-pages.css?v=9')

	def test_admin_login_page_loads_its_own_stylesheet(self):
		response = self.client.get('/admin/login/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'home/css/admin-login.css?v=3')
		self.assertNotContains(response, 'home/css/admin.css?v=3')
		page = response.content.decode()
		self.assertLess(
			page.index('admin/css/login.css'),
			page.index('home/css/admin-login.css?v=3'),
		)
		self.assertContains(response, 'Sign in to manage your Noodle Shop.')

	def test_admin_dashboard_signout_uses_post_and_returns_to_login(self):
		admin_user = User.objects.create_superuser(
			username='admin@example.com',
			email='admin@example.com',
			password='strong-password-123',
		)
		self.client.force_login(admin_user)

		dashboard_response = self.client.get('/admin/')
		self.assertContains(dashboard_response, 'method="post" action="/admin/logout/"')
		self.assertContains(dashboard_response, 'name="next" value="/admin/login/"')

		logout_response = self.client.post('/admin/logout/', {
			'next': '/admin/login/',
		})

		self.assertRedirects(logout_response, '/admin/login/')
		self.assertNotIn('_auth_user_id', self.client.session)

	def test_authenticated_checkout_creates_order_for_admin(self):
		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		self.client.force_login(user)

		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{
				'id': 5,
				'name': 'Client supplied name',
				'price': 1,
				'qty': 2,
				'noodle': 'Thin',
				'egg': True,
			}],
		}), content_type='application/json')

		self.assertEqual(response.status_code, 201)
		order = Order.objects.get()
		self.assertEqual(order.user, user)
		self.assertEqual(order.subtotal, Decimal('120.00'))
		self.assertEqual(order.vat, Decimal('8.40'))
		self.assertEqual(order.total, Decimal('128.40'))
		self.assertEqual(order.items.get().name, 'Chicken noodles')
		self.assertEqual(user.points.points, 12)
		self.assertEqual(response.json()['earned_points'], 12)
		self.assertEqual(response.json()['points_balance'], 12)

	def test_guest_checkout_creates_order_with_catalog_price(self):
		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{
				'id': 5,
				'name': 'Untrusted client name',
				'price': 1,
				'qty': 2,
				'noodle': 'Thin',
				'egg': True,
			}],
		}), content_type='application/json')

		self.assertEqual(response.status_code, 201)
		order = Order.objects.get()
		self.assertIsNone(order.user)
		self.assertEqual(order.subtotal, Decimal('120.00'))
		self.assertEqual(order.vat, Decimal('8.40'))
		self.assertEqual(order.total, Decimal('128.40'))
		self.assertEqual(order.items.get().name, 'Chicken noodles')
		self.assertEqual(response.json()['redirect_url'], f'/bill/?order={order.pk}')
		self.assertIn(order.pk, self.client.session['guest_order_ids'])
		self.assertFalse(UserPoints.objects.exists())

	def test_rewards_api_requires_login_and_returns_catalog(self):
		guest_response = self.client.get('/api/rewards/')
		self.assertEqual(guest_response.status_code, 302)

		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		UserPoints.objects.create(user=user, points=450)
		self.client.force_login(user)

		response = self.client.get('/api/rewards/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {
			'points': 450,
			'rewards': [
				{'product_id': 9, 'name': 'Ice cream', 'points': 300},
				{'product_id': 11, 'name': 'Fried meatballs', 'points': 300},
			],
		})

	def test_guest_cannot_checkout_reward_item(self):
		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{'id': 9, 'qty': 1, 'reward': True}],
		}), content_type='application/json')

		self.assertEqual(response.status_code, 401)
		self.assertEqual(Order.objects.count(), 0)

	def test_reward_checkout_deducts_points_and_earns_only_from_paid_items(self):
		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		UserPoints.objects.create(user=user, points=300)
		self.client.force_login(user)

		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [
				{'id': 9, 'qty': 1, 'reward': True, 'price': 999},
				{'id': 5, 'qty': 2, 'price': 0},
			],
		}), content_type='application/json')

		self.assertEqual(response.status_code, 201)
		order = Order.objects.get()
		self.assertEqual(order.subtotal, Decimal('100.00'))
		self.assertEqual(order.vat, Decimal('7.00'))
		reward_item = order.items.get(product_id=9)
		self.assertEqual(reward_item.price, Decimal('0.00'))
		self.assertTrue(reward_item.is_reward)
		self.assertEqual(order.items.get(product_id=5).price, Decimal('50.00'))
		self.assertEqual(response.json()['points_balance'], 10)
		user.points.refresh_from_db()
		self.assertEqual(user.points.points, 10)
		self.assertEqual(response.json()['reward_points_used'], 300)
		self.assertEqual(response.json()['earned_points'], 10)

	def test_reward_checkout_rejects_insufficient_points_without_order(self):
		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		UserPoints.objects.create(user=user, points=299)
		self.client.force_login(user)

		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{'id': 9, 'qty': 1, 'reward': True}],
		}), content_type='application/json')

		self.assertEqual(response.status_code, 400)
		self.assertIn('Not enough points', response.json()['error'])
		self.assertEqual(Order.objects.count(), 0)
		self.assertEqual(user.points.points, 299)

	def test_checkout_rejects_forged_reward_and_does_not_discount_regular_item(self):
		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		UserPoints.objects.create(user=user, points=500)
		self.client.force_login(user)

		forged_response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{'id': 5, 'qty': 1, 'reward': True}],
		}), content_type='application/json')
		self.assertEqual(forged_response.status_code, 400)
		self.assertEqual(Order.objects.count(), 0)

		regular_response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{'id': 9, 'qty': 1, 'price': 0}],
		}), content_type='application/json')
		self.assertEqual(regular_response.status_code, 201)
		item = Order.objects.get().items.get()
		self.assertEqual(item.price, Decimal('30.00'))
		self.assertFalse(item.is_reward)
		user.points.refresh_from_db()
		self.assertEqual(user.points.points, 503)

	def test_reward_checkout_rejects_quantity_above_one(self):
		user = User.objects.create_user(
			username='customer@example.com',
			email='customer@example.com',
			password='strong-password-123',
		)
		UserPoints.objects.create(user=user, points=600)
		self.client.force_login(user)

		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{'id': 9, 'qty': 2, 'reward': True}],
		}), content_type='application/json')

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Order.objects.count(), 0)
		self.assertEqual(user.points.points, 600)

	def test_guest_cannot_view_points(self):
		response = self.client.get('/api/points/')

		self.assertEqual(response.status_code, 302)
		self.assertIn('/signin/', response.url)

	def test_points_api_creates_zero_balance_for_existing_users(self):
		user = User.objects.create_user(
			username='legacy@example.com',
			email='legacy@example.com',
			password='strong-password-123',
		)
		self.client.force_login(user)

		response = self.client.get('/api/points/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'points': 0})
		self.assertEqual(user.points.points, 0)

	def test_guest_can_view_own_receipt_but_not_another_guest_order(self):
		response = self.client.post('/orders/create/', data=json.dumps({
			'payment': 'Cash',
			'cart': [{'id': 5, 'qty': 1}],
		}), content_type='application/json')
		order_id = Order.objects.get().pk
		self.assertEqual(response.status_code, 201)
		self.assertEqual(self.client.get(f'/bill/?order={order_id}').status_code, 200)

		other_guest = self.client_class()
		self.assertEqual(other_guest.get(f'/bill/?order={order_id}').status_code, 302)


class AIOrderTests(TestCase):
	def test_ai_order_requires_post(self):
		response = self.client.get('/api/ai-order/')

		self.assertEqual(response.status_code, 405)

	@patch('home.views.OpenAI')
	def test_ai_order_requires_server_api_key(self, openai_client):
		with self.settings(OPENROUTER_API_KEY=None):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'Chicken noodles'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 503)
		openai_client.assert_not_called()

	def test_ai_order_rejects_invalid_json(self):
		response = self.client.post(
			'/api/ai-order/',
			data='{',
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn('error', response.json())

	@patch('home.views.OpenAI')
	def test_ai_order_returns_validated_items(self, openai_client):
		openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
			choices=[
				SimpleNamespace(
					message=SimpleNamespace(
						content=json.dumps({
							'items': [{
								'product_id': 5,
								'quantity': 2,
								'noodle': 'Thin',
								'egg': True,
							}],
							'clarification': None,
						}),
					),
				),
			],
		)

		with self.settings(OPENROUTER_API_KEY='test-key'):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'Chicken noodles 2 servings, thin noodles, add egg'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {
			'success': True,
			'items': [{
				'product_id': 5,
				'name': 'Chicken noodles',
				'price': '50.00',
				'quantity': 2,
				'noodle': 'Thin',
				'egg': True,
			}],
		})
		openai_client.assert_called_once_with(
			api_key='test-key',
			base_url='https://openrouter.ai/api/v1',
		)
		openai_client.return_value.chat.completions.create.assert_called_once()
		self.assertEqual(
			openai_client.return_value.chat.completions.create.call_args.kwargs['model'],
			'apodex/apodex-1.1-mini:free',
		)

	@patch('home.views.OpenAI')
	def test_ai_order_places_broad_dessert_request_as_cart_items(self, openai_client):
		openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
			choices=[
				SimpleNamespace(
					message=SimpleNamespace(
						content=json.dumps({
							'items': [{
								'product_id': 9,
								'quantity': 2,
								'noodle': '',
								'egg': False,
							}],
							'clarification': None,
							'assistant_message': None,
						}),
					),
				),
			],
		)

		with self.settings(OPENROUTER_API_KEY='test-key'):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'ขอของหวานสองอย่าง'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['items'], [{
			'product_id': 9,
			'name': 'Ice cream',
			'price': '30.00',
			'quantity': 2,
			'noodle': '',
			'egg': False,
		}])
		prompt = openai_client.return_value.chat.completions.create.call_args.kwargs['messages'][0]['content']
		self.assertIn('broad category request with an explicit quantity is a purchase order', prompt)
		self.assertIn('category: dessert', prompt)

	@patch('home.views.OpenAI')
	def test_ai_order_places_broad_snack_request_as_three_different_items(self, openai_client):
		openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
			choices=[
				SimpleNamespace(
					message=SimpleNamespace(
						content=json.dumps({
							'items': [
								{'product_id': 10, 'quantity': 1, 'noodle': '', 'egg': False},
								{'product_id': 11, 'quantity': 1, 'noodle': '', 'egg': False},
								{'product_id': 12, 'quantity': 1, 'noodle': '', 'egg': False},
							],
							'clarification': None,
							'assistant_message': None,
						}),
					),
				),
			],
		)

		with self.settings(OPENROUTER_API_KEY='test-key'):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'ขอของกินเล่นสักสามอย่าง'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 200)
		items = response.json()['items']
		self.assertEqual([item['product_id'] for item in items], [10, 11, 12])
		self.assertEqual(sum(item['quantity'] for item in items), 3)

	@patch('home.views.OpenAI')
	def test_ai_order_returns_clarification(self, openai_client):
		openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
			choices=[
				SimpleNamespace(
					message=SimpleNamespace(
						content=json.dumps({
							'items': [],
							'clarification': 'Which menu item would you like?',
						}),
					),
				),
			],
		)

		with self.settings(OPENROUTER_API_KEY='test-key'):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'something tasty'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['clarification'], 'Which menu item would you like?')

	@patch('home.views.OpenAI')
	def test_ai_order_returns_menu_recommendation_without_cart_items(self, openai_client):
		recommendation = 'ถ้าชอบรสเข้ม ๆ ลองเมนูต้มยำได้นะครับ แต่สุดท้ายเลือกตามที่ชอบเลย!'
		openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
			choices=[
				SimpleNamespace(
					message=SimpleNamespace(
						content=json.dumps({
							'items': [],
							'clarification': None,
							'assistant_message': recommendation,
						}),
					),
				),
			],
		)

		with self.settings(OPENROUTER_API_KEY='test-key'):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'ช่วยแนะนำเมนูที่อร่อยที่สุดหน่อย'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {
			'success': True,
			'items': [],
			'assistant_message': recommendation,
		})

	@patch('home.views.OpenAI')
	def test_ai_order_rejects_invalid_model_item(self, openai_client):
		openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
			choices=[
				SimpleNamespace(
					message=SimpleNamespace(
						content=json.dumps({
							'items': [{
								'product_id': 999,
								'quantity': 1,
								'noodle': '',
								'egg': False,
							}],
							'clarification': None,
						}),
					),
				),
			],
		)

		with self.settings(OPENROUTER_API_KEY='test-key'):
			response = self.client.post(
				'/api/ai-order/',
				data=json.dumps({'message': 'Mystery food'}),
				content_type='application/json',
			)

		self.assertEqual(response.status_code, 502)

# Create your tests here.
