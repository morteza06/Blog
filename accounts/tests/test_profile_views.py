import pytest
from django.urls import reverse

from accounts.models import CustomUser


@pytest.mark.django_db
def test_profile_view_requires_login(client):
    response = client.get(reverse("profile", args=["testuser"]))
    assert response.status_code == 302  # redirect to login


@pytest.mark.django_db
def test_profile_view_logged_in(client):
    user = CustomUser.objects.create_user(username="a", password="123")
    client.login(username="a", password="123")
    response = client.get(reverse("profile", kwargs={"username": user.username}))
    assert response.status_code == 200
    assert "پروفایل" in response.content.decode()


@pytest.mark.django_db
def test_profile_edit_updates_user(client):
    user = CustomUser.objects.create_user(username="a", password="123")
    client.login(username="a", password="123")

    response = client.post(
        reverse("dashboard"),
        {"first_name": "Ali", "last_name": "Ahmadi", "email": "ali@example.com"},
    )

    user.refresh_from_db()
    assert response.status_code == 302
    assert user.first_name == "Ali"
