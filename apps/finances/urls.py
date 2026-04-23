from django.urls import path

from . import views

app_name = "finances"

urlpatterns = [
    path("", views.finance_dashboard, name="index"),
    path("export/", views.export_budget_excel, name="export"),
]

