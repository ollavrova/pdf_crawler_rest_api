from django.test import TestCase, Client
from pdf_crawler.models import Document
from rest_framework.reverse import reverse


class TestCase(TestCase):

    client = Client()

    def setUp(self):
        Document.objects.create(name='First').save()

    def test_endpoints(self):
        """
        test for endpoints
        """
        self.assertEqual(self.client.get(reverse('pdf_crawler:document-list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('pdf_crawler:document-detail',  kwargs={'pk': 1})).status_code, 200)
        self.assertEqual(self.client.get(reverse('pdf_crawler:url-list')).status_code, 200)
