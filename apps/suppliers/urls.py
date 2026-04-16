from django.urls import path

from . import views

app_name = "suppliers"

urlpatterns = [
    path("", views.supplier_dashboard, name="index"),
    path("profile/", views.supplier_profile_edit, name="profile"),
    path("transactions/", views.supplier_transaction_history, name="history"),
    path("collector/transactions/", views.collector_transaction_list, name="collector_transactions"),
    path("collector/transactions/new/", views.supplier_transaction_create, name="collector_new_transaction"),
]

