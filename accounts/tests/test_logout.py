import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_can_logout(client, django_user_model):
    user = django_user_model.objects.create_user(username='john', password='secret123')
    client.login(username='john', password='secret123')
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('login')
