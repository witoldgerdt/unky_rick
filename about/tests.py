# Create your tests here.
# example_app/tests/test_views.py

from django.test import TestCase
from django.urls import reverse

class AboutPageTest(TestCase):
    def test_about_page_contains_expected_text(self):
        response = self.client.get(reverse('home'))  #  URL name for test
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "expected text")  # 
