from django.urls import path

from . import views

app_name = "reports_admin"

urlpatterns = [
    path("", views.admin_report_list, name="list"),
    path("<int:pk>/", views.admin_report_update, name="update"),
]

