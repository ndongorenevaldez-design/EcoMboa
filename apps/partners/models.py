from django.db import models


class PartnerProfile(models.Model):
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="partner_profile"
    )
    company_name = models.CharField(max_length=180)
    sector = models.CharField(max_length=120, blank=True)
    contact_person = models.CharField(max_length=120, blank=True)
    csr_objectives = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class CollectionContract(models.Model):
    partner = models.ForeignKey(
        PartnerProfile, on_delete=models.CASCADE, related_name="contracts"
    )
    sorting_center = models.ForeignKey(
        "sorting_center.SortingCenter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="partner_contracts",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    target_collection_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    terms = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract #{self.pk} - {self.partner.company_name}"


class CSRReport(models.Model):
    partner = models.ForeignKey(
        PartnerProfile, on_delete=models.CASCADE, related_name="csr_reports"
    )
    reporting_period_start = models.DateField()
    reporting_period_end = models.DateField()
    total_collected_kg = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    co2_avoided_kg = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    impact_summary = models.TextField(blank=True)
    certificate_pdf = models.FileField(upload_to="partners/csr_certificates/", blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSRReport #{self.pk} - {self.partner.company_name}"

