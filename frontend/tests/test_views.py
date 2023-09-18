from django.test import TestCase, Client
from frontend.models import Contact
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class TestContact(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
        self.data = {
            'name': 'test name',
            'email': 'test@example.com',
            'topic': 'test topic',
            'phone': '034567234',
            'message': 'test message',
        }

    def test_contact(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Contact.objects.count(), 1)


class TestUserSignUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user-register')
        self.data = {
            'username': 'testuser',
            'firstname': 'testname',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }

    def test_signup_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(get_user_model().objects.count(), 1)

        created_user = get_user_model().objects.first()
        self.assertEqual(created_user.username, 'testuser')

    def test_signup_failure(self):
        incomplete_data = {
            'username': 'testuser',
            'firstname': 'testname',
            'password1': 'testpassword123',
        }

        response = self.client.post(self.url, incomplete_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', count=1)

        # no user created
        self.assertEqual(get_user_model().objects.count(), 0)


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user-login')
        self.data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        self.user = User.objects.create(
            username='testuser',
            email="testuser@example.com",
            password='testpassword123'
        )

    def test_login_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)


class TestLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user-logout')
        self.user = User.objects.create(
            username='testuser',
            email="testuser@example.com",
            password='testpassword123'
        )
        self.client.login(
            username='testuser',
            password='testpassword123'
        )

    def test_logout_success(self):
        self.assertTrue(self.user.is_authenticated)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        # self.user.refresh_from_db()
        # self.assertTrue(self.user.is_authenticated)


class TestBookDelivery(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('book_delivery')
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        def test_book_delivery(self):
            # login user
            self.client.login(username='testuser', password='testpassword')

            post_data = {
                'item': 'item',
                'item_type': 'book',
                'pickup_location': 'test_pickup_location',
                'destination_location': 'test_destination'
            }

            response = self.client.post(self.url, post_data)
            self.assertRedirects(response, reverse('confirm-delivery'))


class TestTrackOrder(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('track-order')

    def test_track_order(self):
        post_data = {
            'order-number': '23454365456456'
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order-results'))

        def test_track_order_view_with_invalid_order_number(self):
            invalid_order_number = 'INVALID123'

            post_data = {
                'order-number': invalid_order_number,
            }

            response = self.client.post(self.url, post_data)

            self.assertRedirects(response, reverse('order-results'))
            self.assertIsNone(self.client.session.get('status'))
