from django.urls import path

from . import views

app_name = "collection_points"

urlpatterns = [
    path("", views.AdminCollectionPointListView.as_view(), name="admin_list"),
    path("new/", views.AdminCollectionPointCreateView.as_view(), name="admin_create"),
    path("<int:pk>/edit/", views.AdminCollectionPointUpdateView.as_view(), name="admin_update"),
    path("<int:pk>/delete/", views.AdminCollectionPointDeleteView.as_view(), name="admin_delete"),
]

