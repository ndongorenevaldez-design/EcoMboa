from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.access import role_required
from apps.missions.models import Mission

from .forms import AdminReportUpdateForm, ReportMissionAssignmentForm, WasteReportCreateForm
from .models import WasteReport


def _build_timeline(report, mission):
    timeline = [
        {
            "title": "Report submitted",
            "detail": "Citizen report created and awaiting assignment.",
            "at": report.created_at,
            "state": "done",
        }
    ]

    if mission:
        collector_name = "Collector"
        if mission.collector:
            collector_name = mission.collector.get_full_name() or mission.collector.username
        timeline.append(
            {
                "title": "Collector assigned",
                "detail": f"{collector_name} assigned.",
                "at": mission.assigned_at,
                "state": "done",
            }
        )

        if mission.status in {"en_route", "on_site", "collected", "delivered"}:
            timeline.append(
                {
                    "title": "Collection in progress",
                    "detail": "Collector is handling the mission.",
                    "at": mission.collected_at or report.updated_at,
                    "state": "active" if mission.status in {"en_route", "on_site"} else "done",
                }
            )

        if mission.status in {"collected", "delivered"}:
            timeline.append(
                {
                    "title": "Waste collected",
                    "detail": f"Collected weight: {mission.collected_weight_kg or '-'} kg",
                    "at": mission.collected_at or report.updated_at,
                    "state": "done",
                }
            )

        if mission.status == "delivered":
            timeline.append(
                {
                    "title": "Delivered to sorting center",
                    "detail": "Mission marked delivered.",
                    "at": mission.delivered_at or timezone.now(),
                    "state": "done",
                }
            )

    if report.status == "processed":
        timeline.append(
            {
                "title": "Processed",
                "detail": "Waste processed at sorting center.",
                "at": report.updated_at,
                "state": "done",
            }
        )
    elif report.status == "cancelled":
        timeline.append(
            {
                "title": "Cancelled",
                "detail": "This report was cancelled.",
                "at": report.updated_at,
                "state": "cancelled",
            }
        )

    timeline.sort(key=lambda item: item["at"] or timezone.now())
    return timeline


@login_required
@role_required("citizen")
def citizen_report_list(request):
    reports = (
        WasteReport.objects.filter(citizen=request.user)
        .prefetch_related(
            Prefetch(
                "mission_set",
                queryset=Mission.objects.select_related("collector", "destination_center").order_by("-assigned_at"),
            )
        )
        .order_by("-created_at")
    )
    return render(request, "reports/citizen_report_list.html", {"reports": reports})


@login_required
@role_required("citizen")
def citizen_report_create(request):
    if request.method == "POST":
        form = WasteReportCreateForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.citizen = request.user
            report.status = "pending"
            report.save()
            messages.success(request, "Report submitted successfully.")
            return redirect("reports:detail", pk=report.pk)
        messages.error(request, "Please fix the highlighted fields.")
    else:
        form = WasteReportCreateForm()
    return render(request, "reports/citizen_report_form.html", {"form": form})


@login_required
def report_detail(request, pk):
    if request.user.role == "admin":
        report = get_object_or_404(
            WasteReport.objects.select_related("citizen").prefetch_related(
                Prefetch(
                    "mission_set",
                    queryset=Mission.objects.select_related("collector", "destination_center").order_by("-assigned_at"),
                )
            ),
            pk=pk,
        )
    else:
        report = get_object_or_404(
            WasteReport.objects.prefetch_related(
                Prefetch(
                    "mission_set",
                    queryset=Mission.objects.select_related("collector", "destination_center").order_by("-assigned_at"),
                )
            ),
            pk=pk,
            citizen=request.user,
        )
    mission = report.mission_set.first()
    timeline = _build_timeline(report, mission)
    return render(
        request,
        "reports/report_detail.html",
        {"report": report, "mission": mission, "timeline": timeline},
    )


@login_required
@role_required("admin")
def admin_report_list(request):
    status_filter = request.GET.get("status", "").strip()
    urgency = request.GET.get("urgent", "").strip()
    query = request.GET.get("q", "").strip()

    reports = WasteReport.objects.select_related("citizen").prefetch_related(
        Prefetch(
            "mission_set",
            queryset=Mission.objects.select_related("collector").order_by("-assigned_at"),
        )
    )
    if status_filter:
        reports = reports.filter(status=status_filter)
    if urgency == "yes":
        reports = reports.filter(is_urgent=True)
    if query:
        reports = reports.filter(
            Q(citizen__email__icontains=query)
            | Q(citizen__username__icontains=query)
            | Q(district__icontains=query)
            | Q(neighborhood__icontains=query)
        )
    reports = reports.order_by("-is_urgent", "-created_at")
    return render(
        request,
        "reports/admin_report_list.html",
        {"reports": reports, "status_filter": status_filter, "urgency": urgency, "query": query},
    )


@login_required
@role_required("admin")
def admin_report_update(request, pk):
    report = get_object_or_404(WasteReport.objects.select_related("citizen"), pk=pk)
    mission = (
        Mission.objects.select_related("collector", "destination_center")
        .filter(report=report)
        .order_by("-assigned_at")
        .first()
    )

    if request.method == "POST":
        report_form = AdminReportUpdateForm(request.POST, instance=report, prefix="report")
        assign_form = ReportMissionAssignmentForm(request.POST, prefix="assign")
        if report_form.is_valid() and assign_form.is_valid():
            report = report_form.save()
            collector = assign_form.cleaned_data["collector"]
            destination_center = assign_form.cleaned_data["destination_center"]
            mission_status = assign_form.cleaned_data["mission_status"]
            notes = assign_form.cleaned_data["notes"]

            if mission:
                mission.collector = collector
                mission.destination_center = destination_center
                mission.status = mission_status
                mission.notes = notes
                mission.save()
            else:
                mission = Mission.objects.create(
                    source_type="report",
                    report=report,
                    collector=collector,
                    destination_center=destination_center,
                    status=mission_status,
                    notes=notes,
                )

            if mission_status in {"assigned", "en_route", "on_site"}:
                report.status = "assigned"
            elif mission_status in {"collected", "delivered"}:
                report.status = "collected"
            report.save(update_fields=["status", "updated_at"])
            messages.success(request, "Report and assignment updated.")
            return redirect("reports_admin:list")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        report_form = AdminReportUpdateForm(instance=report, prefix="report")
        assign_initial = {}
        if mission:
            assign_initial = {
                "collector": mission.collector_id,
                "destination_center": mission.destination_center_id,
                "mission_status": mission.status,
                "notes": mission.notes,
            }
        assign_form = ReportMissionAssignmentForm(initial=assign_initial, prefix="assign")

    return render(
        request,
        "reports/admin_report_update.html",
        {"report": report, "mission": mission, "report_form": report_form, "assign_form": assign_form},
    )
