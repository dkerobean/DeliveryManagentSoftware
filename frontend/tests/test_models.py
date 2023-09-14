from django.test import TestCase
from frontend.models import Contact
# from django.contrib.auth.models import User


class ContactTestCase(TestCase):

    def test_contact_creations(self):
        contact = Contact.objects.create(
            name='John',
            topic='topic',
            email='email@example.com',
            phone='5675675756',
            message='lorem ipsum dolor sit amet, consectetur adipiscing',
        )

        self.assertEqual(contact.name, 'John')
        self.assertEqual(contact.topic, 'topic')
        self.assertEqual(contact.email, 'email@example.com'),
        self.assertEqual(contact.phone, '5675675756'),
        self.assertEqual(contact.message, 'lorem ipsum dolor sit amet,\
                         consectetur adipiscing'),

    def test_str_method(self):
        # Create a Contact instance
        contact = Contact.objects.create(
            name='Jane Smith',
            topic='Support Request',
            email='janesmith@example.com',
            phone='9876543210',
            message='Another test message.'
        )

        # Check the __str__ method
        self.assertEqual(str(contact), 'Jane Smith')
