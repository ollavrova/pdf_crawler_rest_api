from django.test import TestCase, Client
from rest_framework.reverse import reverse


class TestCase(TestCase):

    client = Client()

    def test_endpoints(self):
        """
        test for endpoints
        """
        self.assertEqual(self.client.get(reverse('pdf_crawler:home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('pdf_crawler:documents-list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('pdf_crawler:documents-detail')).status_code, 200)
        self.assertEqual(self.client.get(reverse('pdf_crawler:urls-list')).status_code, 200)
