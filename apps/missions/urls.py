from django.urls import path

from . import views

app_name = "missions"

urlpatterns = [
    path("", views.mission_list, name="index"),
    path("dashboard/", views.collector_dashboard, name="dashboard"),
    path("<int:pk>/", views.mission_detail, name="detail"),
    path("<int:pk>/status/", views.mission_status_update, name="status_update"),
    path("<int:pk>/confirm/", views.mission_confirm_collection, name="confirm"),
]

