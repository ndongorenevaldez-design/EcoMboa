from django.http import HttpResponse
from django.urls import path

app_name = "sorting_center"

urlpatterns = [
    path("", lambda request: HttpResponse("Sorting center placeholder."), name="index"),
]

