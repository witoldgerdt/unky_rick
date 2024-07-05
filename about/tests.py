# about/tests.py

from django.test import TestCase
from django.urls import reverse

class AboutPageTest(TestCase):
    def test_about_page_contains_expected_text(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who is Unky Rick?")
