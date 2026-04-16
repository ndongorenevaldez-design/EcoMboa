from django.http import HttpResponse
from django.urls import path

app_name = "buyers"

urlpatterns = [
    path("", lambda request: HttpResponse("Buyers placeholder."), name="index"),
]

