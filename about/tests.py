import os
import pytest
from django.urls import reverse

@pytest.mark.skipif(os.getenv('GITHUB_ACTIONS') is None, reason="Skipping this test locally")
@pytest.mark.django_db
class TestAboutPage:
    def test_about_page_contains_expected_text(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert "Who is Unky Rick?" in response.content.decode()
