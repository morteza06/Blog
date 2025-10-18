import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_shows_recent_posts_and_notifications(client, django_user_model):
    user = django_user_model.objects.create_user(username="u1", password="1234")
    client.login(username="u1", password="1234")

    # create posts
    for i in range(3):
        user.posts.create(title=f"Post {i}", content="x")

    # create notifications
    from accounts.models import Notification

    Notification.objects.create(user=user, title="Sys msg", message="Hello")

    resp = client.get(reverse("dashboard"))
    assert resp.status_code == 200
    assert b"Post 0" in resp.content or b"Post 1" in resp.content
    assert b"Sys msg" in resp.content
