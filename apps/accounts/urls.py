from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("redirect/", views.role_redirect, name="role_redirect"),
    path("profile/", views.profile_view, name="profile"),
]

