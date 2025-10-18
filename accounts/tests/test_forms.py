import datetime

import pytest

from accounts.forms import ProfileEditForm
from accounts.models import CustomUser


@pytest.mark.django_db
def test_birth_date_validation():
    user = CustomUser.objects.create_user(username="testuser", password="pass123")

    # تاریخ آینده → خطا
    form_data = {"birth_date": datetime.date.today() + datetime.timedelta(days=1)}
    form = ProfileEditForm(data=form_data, instance=user)
    assert not form.is_valid()
    assert "تاریخ تولد نمی‌تواند بزرگتر از امروز باشد." in form.errors["birth_date"]

    # تاریخ خیلی قدیمی → خطا
    form_data = {"birth_date": datetime.date(1800, 1, 1)}
    form = ProfileEditForm(data=form_data, instance=user)
    assert not form.is_valid()
    assert "تاریخ تولد باید بعد از سال 1900 باشد." in form.errors["birth_date"]

    # تاریخ معتبر → OK
    form_data = {"birth_date": datetime.date(1990, 5, 20)}
    form = ProfileEditForm(data=form_data, instance=user)
    assert form.is_valid()
