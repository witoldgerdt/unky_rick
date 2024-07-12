from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_money_page_contains_expected_text(client):
    response = client.get(reverse('money'))
    assert response.status_code == 200
    assert "This is the money page." in response.content.decode()