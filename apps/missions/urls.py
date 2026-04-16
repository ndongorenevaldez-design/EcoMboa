from django.http import HttpResponse
from django.urls import path

app_name = "missions"

urlpatterns = [
    path("", lambda request: HttpResponse("Missions placeholder."), name="index"),
]

