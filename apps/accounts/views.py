from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProfileUpdateForm


ROLE_REDIRECT_MAP = {
    "citizen": "reports:index",
    "seller": "suppliers:index",
    "collector": "missions:index",
    "center": "sorting_center:index",
    "buyer": "buyers:index",
    "partner": "partners:index",
    "admin": "dashboard:index",
}


@login_required
def role_redirect(request: HttpRequest) -> HttpResponse:
    route_name = ROLE_REDIRECT_MAP.get(getattr(request.user, "role", ""), "accounts:profile")
    return redirect(reverse(route_name))


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect("accounts:profile")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
