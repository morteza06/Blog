from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, label="انتشار فوری")

    class Meta:
        model = Post
        fields = ["title", "content", "tags", "status", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-select"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "نظر خود را اینجا بنویسید...",
                    "rows": 3,
                }
            )
        }
        labels = {"content": "ویرایش نظر"}
