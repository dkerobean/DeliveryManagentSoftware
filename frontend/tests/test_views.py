from django.test import TestCase, Client
from frontend.models import Contact
from django.urls import reverse
from django.contrib.auth import get_user_model


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

    def test_login_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
