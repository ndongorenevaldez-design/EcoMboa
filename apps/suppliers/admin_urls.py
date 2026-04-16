from django.urls import path

from . import views

app_name = "suppliers_admin"

urlpatterns = [
    path("approvals/", views.admin_supplier_approvals, name="approvals"),
    path("approvals/<int:pk>/approve/", views.admin_supplier_approve, name="approve"),
]

