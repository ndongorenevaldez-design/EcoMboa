# Generated manually for admin portal bootstrap

from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_admin_user(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    user, created = User.objects.get_or_create(
        email="admin@gmail.com",
        defaults={
            "username": "admin",
            "role": "admin",
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )
    user.username = user.username or "admin"
    user.role = "admin"
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.password = make_password("Admin1234")
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_admin_user, migrations.RunPython.noop),
    ]

