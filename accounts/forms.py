from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
            "birth_data": forms.DateInput(attrs={"class": "form", "type": "date"}),
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
        # TODO: در آینده اعتبارسنجی ایمیل تکراری یا فرمت تاریخ را اضافه کنیم
