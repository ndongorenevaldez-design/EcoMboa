from allauth.account.signals import email_confirmed, user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def assign_default_role(sender, request, user, **kwargs):
    if not user.role:
        user.role = "citizen"
        user.save(update_fields=["role"])


@receiver(email_confirmed)
def mark_user_verified(sender, request, email_address, **kwargs):
    user = email_address.user
    if not user.is_verified:
        user.is_verified = True
        user.save(update_fields=["is_verified"])

