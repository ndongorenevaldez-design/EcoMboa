from django.http import HttpResponse
from django.urls import path

app_name = "public"

urlpatterns = [
    path("", lambda request: HttpResponse("EcoMboa home placeholder."), name="home"),
]

