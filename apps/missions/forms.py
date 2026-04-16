from django import forms
from django.utils import timezone

from .models import Mission


class MissionStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ["status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class MissionConfirmationForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ["collected_weight_kg", "confirmation_photo", "notes"]
        widgets = {
            "collected_weight_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

    def save(self, commit=True):
        mission = super().save(commit=False)
        if mission.status in {"assigned", "en_route", "on_site"}:
            mission.status = "collected"
        if not mission.collected_at:
            mission.collected_at = timezone.now()
        if commit:
            mission.save()
        return mission

