from django.urls import path

from . import views

app_name = "buyers"

urlpatterns = [
    path("", views.buyer_dashboard, name="index"),
    path("profile/", views.buyer_profile_edit, name="profile"),
    path("catalog/", views.material_catalog, name="catalog"),
]

