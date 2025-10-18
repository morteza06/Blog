import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_email_unique_validation(client, django_user_model):
    User = django_user_model
    User.objects.create_user(username="a", email="a@example.com", password="123")
    User.objects.create_user(username="b", email="b@example.com", password="123")
    client.login(username="b", password="123")

    url = reverse("profile_edit")
    resp = client.post(
        url,
        {"email": "a@example.com", "first_name": "X", "last_name": "Y"},
    )
    assert resp.status_code == 200  # form invalid -> show form
    content = resp.content.decode("utf-8")
    assert "این ایمیل قبلا استفاده شده است.  " in content
