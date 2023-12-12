from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Secret
from .utils import get_note_id


class GenerateSecretViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_secret(self):
        url = reverse('generate_secret')
        data = {'secret_text': 'Hello', 'code_phrase': 'World'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('secret_key', response.json())

        secret_key = response.json()['secret_key']
        expected_note_id = get_note_id("Hello", "World")
        self.assertEqual(secret_key, expected_note_id)

    def test_generate_secret_invalid_data(self):
        url = reverse('generate_secret')
        data = {'secret_text': 'Hello', 'code_phrase': ''}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SecretViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.secret = Secret.objects.create(
                            secret_text='Hello', 
                            code_phrase='World', 
                            secret_key=get_note_id('Hello', 'World')
                        )

    def test_reveal_secret(self):
        url = reverse('reveal_secret', args=[self.secret.secret_key])
        data = {'code_phrase': 'World'}
        response = self.client.get(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('secret_text', response.json())
        self.secret.refresh_from_db()
        self.assertEqual(self.secret.is_revealed, True)
        
    def test_reveal_secret_invalid_code_phrase(self):
        url = reverse('reveal_secret', args=[self.secret.secret_key])
        data = {'code_phrase': 'Invalid'}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertEqual(self.secret.is_revealed, False)

    def test_reveal_already_revealed_secret(self):
        self.secret.is_revealed = True
        self.secret.save()

        url = reverse('reveal_secret', args=[self.secret.secret_key])
        data = {'code_phrase': 'World'}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertEqual(self.secret.is_revealed, True)

# python manage.py test src.core.tests