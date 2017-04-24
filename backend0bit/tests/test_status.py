from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestStatusView(APITestCase):
    def test_status(self):
        url = reverse('status')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'"OK"')
