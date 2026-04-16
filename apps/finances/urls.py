from django.http import HttpResponse
from django.urls import path

app_name = "finances"

urlpatterns = [
    path("", lambda request: HttpResponse("Finances placeholder."), name="index"),
]

