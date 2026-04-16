import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.access import role_required

from .forms import MissionConfirmationForm, MissionStatusUpdateForm
from .models import Mission


def _mission_location(mission):
    if mission.report_id:
        return mission.report.latitude, mission.report.longitude
    if mission.collection_point_id:
        return mission.collection_point.latitude, mission.collection_point.longitude
    return None, None


def _can_access_mission(user, mission):
    return user.role == "admin" or (user.role == "collector" and mission.collector_id == user.id)


@login_required
@role_required("collector", "admin")
def mission_list(request):
    missions = Mission.objects.select_related(
        "collector", "report", "collection_point", "destination_center"
    )
    if request.user.role == "collector":
        missions = missions.filter(collector=request.user)
    missions = missions.order_by("-assigned_at")
    return render(request, "missions/mission_list.html", {"missions": missions})


@login_required
@role_required("collector", "admin")
def mission_detail(request, pk):
    mission = get_object_or_404(
        Mission.objects.select_related(
            "collector", "report", "collection_point", "destination_center"
        ),
        pk=pk,
    )
    if not _can_access_mission(request.user, mission):
        return HttpResponseForbidden("You cannot access this mission.")
    lat, lng = _mission_location(mission)
    return render(
        request,
        "missions/mission_detail.html",
        {"mission": mission, "lat": lat, "lng": lng},
    )


@login_required
@role_required("collector", "admin")
def mission_status_update(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if not _can_access_mission(request.user, mission):
        return HttpResponseForbidden("You cannot update this mission.")

    if request.method == "POST":
        form = MissionStatusUpdateForm(request.POST, instance=mission)
        if form.is_valid():
            mission = form.save(commit=False)
            if mission.status in {"en_route", "on_site"} and not mission.collected_at:
                mission.collected_at = None
            if mission.status == "delivered" and not mission.delivered_at:
                mission.delivered_at = timezone.now()
            mission.save()
            if mission.report:
                if mission.status == "delivered":
                    mission.report.status = "processed"
                elif mission.status == "collected":
                    mission.report.status = "collected"
                elif mission.status in {"assigned", "en_route", "on_site"}:
                    mission.report.status = "assigned"
                elif mission.status == "cancelled":
                    mission.report.status = "cancelled"
                mission.report.save(update_fields=["status", "updated_at"])
            messages.success(request, "Mission status updated.")
            return redirect("missions:detail", pk=mission.pk)
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = MissionStatusUpdateForm(instance=mission)

    return render(
        request,
        "missions/mission_status_form.html",
        {"mission": mission, "form": form},
    )


@login_required
@role_required("collector", "admin")
def mission_confirm_collection(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if not _can_access_mission(request.user, mission):
        return HttpResponseForbidden("You cannot confirm this mission.")

    if request.method == "POST":
        form = MissionConfirmationForm(request.POST, request.FILES, instance=mission)
        if form.is_valid():
            mission = form.save()
            if mission.report:
                mission.report.status = "collected"
                mission.report.save(update_fields=["status", "updated_at"])
            messages.success(request, "Collection confirmation saved.")
            return redirect("missions:detail", pk=mission.pk)
        messages.error(request, "Please fix the highlighted fields.")
    else:
        form = MissionConfirmationForm(instance=mission)

    return render(
        request,
        "missions/mission_confirm.html",
        {"mission": mission, "form": form},
    )


@login_required
@role_required("collector", "admin")
def collector_dashboard(request):
    now = timezone.localtime()
    today = now.date()
    missions = Mission.objects.select_related("report", "collection_point", "destination_center").filter(
        Q(assigned_at__date=today) | Q(status__in=["assigned", "en_route", "on_site", "collected"])
    )
    if request.user.role == "collector":
        missions = missions.filter(collector=request.user)
    missions = missions.order_by("-assigned_at")

    map_items = []
    for mission in missions:
        lat, lng = _mission_location(mission)
        if lat is None or lng is None:
            continue
        label = (
            mission.report.text_address
            if mission.report_id
            else (mission.collection_point.address if mission.collection_point_id else "Unknown location")
        )
        map_items.append(
            {
                "id": mission.id,
                "lat": float(lat),
                "lng": float(lng),
                "status": mission.get_status_display(),
                "source": mission.get_source_type_display(),
                "label": label,
            }
        )

    return render(
        request,
        "missions/collector_dashboard.html",
        {"missions": missions, "map_items_json": json.dumps(map_items)},
    )

