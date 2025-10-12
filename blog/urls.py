from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post_detail, name='post_detail'),   
    path("new/", views.post_create, name="post_create"),
]
