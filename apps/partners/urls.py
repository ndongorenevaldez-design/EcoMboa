from django.urls import path

from . import views

app_name = "partners"

urlpatterns = [
    path("", views.partner_dashboard, name="index"),
    path("profile/", views.partner_profile_edit, name="profile"),
]

