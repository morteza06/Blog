import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_landing_page_loads_successfully(client):
    """بررسی اینکه صفحه لندینگ بدون خطا باز شود"""
    url = reverse("landing:landing")
    response = client.get(url)
    assert response.status_code == 200
    assert "خوش آمدید" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_landing_page_template_used(client):
    """بررسی اینکه تمپلیت صحیح استفاده شود"""
    url = reverse("landing:landing")
    response = client.get(url)
    assert "landing/index.html" in [t.name for t in response.templates]
