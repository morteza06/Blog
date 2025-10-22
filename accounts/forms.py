import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from PIL import Image

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


def validate_image(image):
    max_size = 2 * 1024 * 1024  # ۲ مگابایت
    valid_extensions = ["jpg", "jpeg", "png"]

    # بررسی نوع فایل
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("فرمت فایل باید JPG یا PNG باشد.")

    # بررسی حجم فایل
    if image.size > max_size:
        raise ValidationError("حجم تصویر نباید بیش از ۲ مگابایت باشد.")

    # بررسی ابعاد تصویر
    img = Image.open(image)
    width, height = img.size
    if width > 2000 or height > 2000:
        raise ValidationError(
            "ابعاد تصویر بیش از حد بزرگ است (حداکثر 2000x2000 پیکسل)."
        )


class CustomClearableFileInput(ClearableFileInput):
    template_name = "widgets/custom_clearable_file_input.html"


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label="نام",
        required=True,
        error_messages={"required": "لطفاً نام خود را وارد کنید."},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام خود را وارد کنید"}
        ),
    )

    last_name = forms.CharField(
        label="نام خانوادگی",
        required=True,
        error_messages={"required": "لطفاً نام خانوادگی خود را وارد کنید."},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی خود را وارد کنید",
            }
        ),
    )

    display_name = forms.CharField(
        label="نام نمایشی",
        required=True,
        error_messages={"required": "نام نمایشی الزامی است."},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نامی که در پروفایل نمایش داده می‌شود",
            }
        ),
    )

    email = forms.EmailField(
        label="ایمیل",
        required=True,
        error_messages={
            "required": "لطفاً ایمیل خود را وارد کنید.",
            "invalid": "ایمیل معتبر نیست.",
        },
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل خود را وارد کنید"}
        ),
    )

    avatar = forms.ImageField(
        label="عکس پروفایل",
        required=False,
        validators=[validate_image],
        widget=CustomClearableFileInput(
            attrs={
                "class": "form-control-file",
                "placeholder": "تصویر خود را انتخاب کنید",
            }
        ),
    )

    birth_date = forms.DateField(
        label="تاریخ تولد",
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
    )

    profile_note = forms.CharField(
        label="پیام پروفایل",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "چیزی درباره خودت بنویسید...",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "display_name",
            "avatar",
            "birth_date",
            "email",
            "profile_note",
        ]

    # تغییر برچسب‌ها
    first_name = forms.CharField(
        label="نام", error_messages={"required": "لطفاً نام خود را وارد کنید."}
    )

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

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError("حجم تصویر نباید بیش از ۲ مگابایت باشد.")
        return avatar
