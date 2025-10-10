import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_dashboard_requires_login(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302  # Redirects to login page

@pytest.mark.django_db
def test_dashboard_for_logged_in_user(client, django_user_model):
    user = django_user_model.objects.create_user(username='test', password='12345')
    client.login(username='test', password='12345')
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert b'Dashboard' in response.content
