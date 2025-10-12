from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post_detail, name='post_detail'),   
    path("new/", views.post_create, name="post_create"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]
