from django.urls import path

from . import views

app_name = "partners_admin"

urlpatterns = [
    path("contracts/", views.admin_contract_list, name="contracts"),
    path("contracts/new/", views.admin_contract_create, name="contract_create"),
    path("csr/new/", views.admin_csr_report_create, name="csr_create"),
]

