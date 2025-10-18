import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TimeInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "from-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "display_name",
            "avatar",
            "birth_date",
            "email",
            "profile_note",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "from-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "birth_data": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "min": "1900-01-01",
                    "max": datetime.date.today().isoformat(),  # تاریخ امروز
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email address"}
            ),
            "profile_note": forms.Textarea(
                attrs={
                    "class": "from-control",
                    "rows": 4,
                    "placeholder": "Personal note or message",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            # (فاصله، حروف بزرگ/کوچک، فضاهای اضافی)  error finding
            email_normalized = email.strip().lower()
            # بررسی تکراری بودن ایمیل برای کاربران دیگر
            qs = User.objects.filter(email__iexact=email_normalized).exclude(
                pk=self.instance.pk
            )
            if qs.exists():
                raise forms.ValidationError("این ایمیل قبلا استفاده شده است.  ")
            return email_normalized
        return email

    def clean_birth_date(self):
        bd = self.cleaned_data.get("birth_date")
        if bd:
            if bd > datetime.date.today():
                raise ValidationError("تاریخ تولد نمی‌تواند بزرگتر از امروز باشد.")
            if bd < datetime.date(1900, 1, 1):
                raise ValidationError("تاریخ تولد باید بعد از سال 1900 باشد.")
        return bd
