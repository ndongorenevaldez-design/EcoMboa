from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "public"

urlpatterns = [
    path("", TemplateView.as_view(template_name="public/home.html"), name="home"),
    path("points/", views.PublicCollectionPointListView.as_view(), name="points"),
    path("points/<int:pk>/", views.PublicCollectionPointDetailView.as_view(), name="point_detail"),
    path("map/", views.PublicCollectionMapView.as_view(), name="map"),
]
