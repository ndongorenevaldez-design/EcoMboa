from django.http import HttpResponse
from django.urls import path

app_name = "reports"

urlpatterns = [
    path("", lambda request: HttpResponse("Reports placeholder."), name="index"),
]

