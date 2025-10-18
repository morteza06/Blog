from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
        ),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="blog:home"), name="logout"
    ),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("notifications/", views.notifications_list, name="notifications"),
    path(
        "notifications/mark_read/<int:pk>/",
        views.notification_mark_read,
        name="notification_mark_read",
    ),
    path("profile/<str:username>/", views.profile_view, name="profile"),
]
