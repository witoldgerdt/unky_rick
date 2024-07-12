from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_about_page_button_redirects_to_money(client):
    response = client.get(reverse('about'))
    assert response.status_code == 200
    assert "To cultivate a new mindset." in response.content.decode()

@pytest.mark.django_db
def test_money_page_contains_expected_text(client):
    response = client.get(reverse('money'))
    assert response.status_code == 200
    assert "Money Page" in response.content.decode()