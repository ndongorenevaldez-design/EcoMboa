from django import forms

from apps.accounts.models import User
from apps.missions.models import Mission
from apps.sorting_center.models import SortingCenter

from .models import WasteReport


class WasteReportCreateForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = [
            "waste_type",
            "description",
            "photo",
            "latitude",
            "longitude",
            "text_address",
            "district",
            "neighborhood",
            "estimated_quantity_kg",
            "is_urgent",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "latitude": forms.NumberInput(attrs={"step": "any", "readonly": "readonly"}),
            "longitude": forms.NumberInput(attrs={"step": "any", "readonly": "readonly"}),
            "estimated_quantity_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class AdminReportUpdateForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = [
            "status",
            "is_urgent",
            "estimated_quantity_kg",
            "district",
            "neighborhood",
            "text_address",
            "description",
            "points_awarded",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "estimated_quantity_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1"}),
            "points_awarded": forms.NumberInput(attrs={"min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class ReportMissionAssignmentForm(forms.Form):
    collector = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=True,
        label="Collector",
    )
    destination_center = forms.ModelChoiceField(
        queryset=SortingCenter.objects.filter(is_active=True).order_by("name"),
        required=False,
        label="Destination sorting center",
    )
    mission_status = forms.ChoiceField(choices=Mission.STATUSES, initial="assigned")
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["collector"].queryset = User.objects.filter(role="collector").order_by(
            "first_name", "last_name", "username"
        )
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

