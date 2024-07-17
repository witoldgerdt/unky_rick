import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_money_page_contains_expected_text(client):
    response = client.get(reverse('money'))
    assert response.status_code == 200
    assert "Money Page" in response.content.decode()
