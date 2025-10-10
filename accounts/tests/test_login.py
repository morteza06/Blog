import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_can_login(client, django_user_model):
    user = django_user_model.objects.create_user(username='john', password='secret123')
    url = reverse('login')
    response = client.post(url, {'username': 'john', 'password': 'secret123'})
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
