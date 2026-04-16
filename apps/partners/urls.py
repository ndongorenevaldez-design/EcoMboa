from django.http import HttpResponse
from django.urls import path

app_name = "partners"

urlpatterns = [
    path("", lambda request: HttpResponse("Partners placeholder."), name="index"),
]

