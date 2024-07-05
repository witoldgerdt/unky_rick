# about/tests.py

from django.test import TestCase
from django.urls import reverse

class AboutPageTest(TestCase):
    def test_about_page_contains_expected_text(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who is Unky Rick?")
        # self.assertContains(response, "During the summer holidays after the school year, your parents send you to stay with a distant relative you met a long time ago when you were a kid.")
