from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.admin_dashboard, name="index"),
    path("portal/", views.admin_portal_login, name="portal_login"),
    path("logout/", views.admin_portal_logout, name="portal_logout"),
]

