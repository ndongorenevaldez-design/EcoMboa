from django.http import HttpResponse
from django.urls import path

app_name = "suppliers"

urlpatterns = [
    path("", lambda request: HttpResponse("Suppliers placeholder."), name="index"),
]

