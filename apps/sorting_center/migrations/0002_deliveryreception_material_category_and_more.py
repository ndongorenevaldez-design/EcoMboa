# Generated manually for Phase 8 sorting center workflow

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sorting_center", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliveryreception",
            name="material_category",
            field=models.CharField(
                choices=[
                    ("plastic", "Plastic"),
                    ("metal", "Metal"),
                    ("paper", "Paper"),
                    ("glass", "Glass"),
                    ("organic", "Organic"),
                    ("textile", "Textile"),
                    ("ewaste", "E-Waste"),
                ],
                default="plastic",
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="deliveryreception",
            name="quality_grade",
            field=models.CharField(
                choices=[("A", "Grade A"), ("B", "Grade B"), ("C", "Grade C")],
                default="B",
                max_length=1,
            ),
            preserve_default=False,
        ),
    ]

