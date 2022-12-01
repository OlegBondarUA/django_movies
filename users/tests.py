from unittest import TestCase

from django.test import Client


class UserTestCase(TestCase):

    def test_client(self):
        client = Client()
        response = client.post('/login/', {'username': 'john', 'password': 'smith'})
        result = response.status_code
        self.assertEqual(result, 200)

    def test_content(self):
        client = Client()
        response = client.get('/login/')
        result = response.content
        self.assertEqual(type(result), bytes)