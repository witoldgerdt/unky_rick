import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_about_page_contains_expected_text(client):
    response = client.get(reverse('about'))
    assert response.status_code == 200
    assert "Who is Unky Rick?" in response.content.decode()
