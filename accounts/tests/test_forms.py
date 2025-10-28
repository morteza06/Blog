import datetime

import pytest

from accounts.forms import ProfileEditForm
from accounts.models import CustomUser


@pytest.mark.django_db
def test_birth_date_validation():
    user = CustomUser.objects.create_user(username="testuser", password="pass123")

    form_data = {"birth_date": datetime.date(1990, 5, 20), "email": "test@example.com"}
    form = ProfileEditForm(data=form_data, instance=user)
    assert form.is_valid()
