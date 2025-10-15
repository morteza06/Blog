import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_profile_edit_updates_display_name(client, django_user_model):
    user = django_user_model.objects.create_user(username="user1", password="pass123")
    client.login(username="user1", password="pass123")

    url = reverse("profile_edit")
    response = client.post(
        url,
        {
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "display_name": "AliDev",
            "email": "ali@example.com",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 302
    assert user.display_name == "AliDev"
