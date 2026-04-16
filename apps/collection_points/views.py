from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.accounts.access import RoleRequiredMixin

from .forms import CollectionPointForm
from .models import CollectionPoint


class PublicCollectionPointListView(ListView):
    model = CollectionPoint
    template_name = "collection_points/public_list.html"
    context_object_name = "points"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        qs = CollectionPoint.objects.filter(status="active").order_by("name")
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(district__icontains=query)
                | Q(neighborhood__icontains=query)
            )
        return qs


class PublicCollectionPointDetailView(DetailView):
    model = CollectionPoint
    template_name = "collection_points/public_detail.html"
    context_object_name = "point"


class PublicCollectionMapView(ListView):
    model = CollectionPoint
    template_name = "collection_points/public_map.html"
    context_object_name = "points"

    def get_queryset(self):
        return CollectionPoint.objects.filter(status="active").order_by("name")


class AdminCollectionPointListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = ("admin",)
    model = CollectionPoint
    template_name = "collection_points/admin_list.html"
    context_object_name = "points"
    paginate_by = 20

    def get_queryset(self):
        return CollectionPoint.objects.select_related("manager").order_by("-created_at")


class AdminCollectionPointCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ("admin",)
    model = CollectionPoint
    form_class = CollectionPointForm
    template_name = "collection_points/admin_form.html"
    success_url = reverse_lazy("collection_points:admin_list")

    def form_valid(self, form):
        messages.success(self.request, "Collection point created successfully.")
        return super().form_valid(form)


class AdminCollectionPointUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ("admin",)
    model = CollectionPoint
    form_class = CollectionPointForm
    template_name = "collection_points/admin_form.html"
    success_url = reverse_lazy("collection_points:admin_list")

    def form_valid(self, form):
        messages.success(self.request, "Collection point updated successfully.")
        return super().form_valid(form)


class AdminCollectionPointDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ("admin",)
    model = CollectionPoint
    template_name = "collection_points/admin_confirm_delete.html"
    success_url = reverse_lazy("collection_points:admin_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Collection point deleted successfully.")
        return super().delete(request, *args, **kwargs)

