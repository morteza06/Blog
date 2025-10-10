import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_can_signup(client):
    url = reverse('signup')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'StrongPass123',
        'password2': 'StrongPass123'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after signup
    assert User.objects.filter(username='testuser').exists()
