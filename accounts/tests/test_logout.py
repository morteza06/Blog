import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_can_logout(client, django_user_model):
    django_user_model.objects.create_user(username="john", password="secret123")
    client.login(username="john", password="secret123")
    url = reverse("logout")
    response = client.post(url)
    # NOTE: اگر next_page='home' در LogoutView تنظیم شده باشد:
    assert response.status_code == 302
    assert response.url == reverse("home")
