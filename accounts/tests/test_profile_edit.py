import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_profile_edit_updates_display_name(client, django_user_model):
    user = django_user_model.objects.create_user(username="user1", password="pass123")
    client.login(username="user1", password="pass123")

    url = reverse("dashboard")
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


@pytest.mark.django_db
def test_profile_edit_post(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="pass123"
    )
    client.force_login(user)

    url = reverse("dashboard")  # ← URL همان داشبورد است
    data = {
        "first_name": "Ali",
        "last_name": "Rezaei",
        "display_name": "AliR",
        "email": "ali@example.com",
        "profile_note": "سلام",
    }

    response = client.post(url, data, follow=True)  # follow=True برای مشاهده پیام‌ها
    user.refresh_from_db()

    assert response.status_code == 200
    assert "پروفایل با موفقیت ویرایش شد" in response.content.decode()
    assert user.first_name == "Ali"
    assert user.profile_note == "سلام"
