from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.citizen_report_list, name="index"),
    path("new/", views.citizen_report_create, name="create"),
    path("<int:pk>/", views.report_detail, name="detail"),
    path("admin/manage/", views.admin_report_list, name="admin_list"),
    path("admin/manage/<int:pk>/", views.admin_report_update, name="admin_update"),
]

