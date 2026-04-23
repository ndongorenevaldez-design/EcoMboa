from django.urls import path

from . import views

app_name = "sorting_center"

urlpatterns = [
    path("", views.center_dashboard, name="index"),
    path("receptions/new/", views.delivery_reception_create, name="reception_create"),
    path("receptions/", views.reception_history, name="reception_history"),
    path("stocks/new/", views.stock_edit, name="stock_create"),
]

