from django import forms
from django.utils.text import slugify
from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm

from .models import User


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()
            field.widget.attrs.setdefault("placeholder", field.label)


class CustomSignupForm(StyledFormMixin, SignupForm):
    role = forms.ChoiceField(
        choices=[(k, v) for k, v in User.ROLES if k != "admin"],
        label="I am signing up as",
    )
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=20, required=False)

    def save(self, request):
        user = super().save(request)
        email_prefix = (user.email or "user").split("@")[0]
        base_username = slugify(email_prefix) or "user"
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exclude(pk=user.pk).exists():
            username = f"{base_username}-{counter}"
            counter += 1

        user.username = username
        user.role = self.cleaned_data["role"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone = self.cleaned_data.get("phone", "")
        user.save(
            update_fields=["username", "role", "first_name", "last_name", "phone"]
        )
        return user


class CustomLoginForm(StyledFormMixin, LoginForm):
    pass


class CustomResetPasswordForm(StyledFormMixin, ResetPasswordForm):
    pass


class ProfileUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "address",
            "latitude",
            "longitude",
            "mobile_money_operator",
            "mobile_money_number",
            "profile_photo",
        ]
