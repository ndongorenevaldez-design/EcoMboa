from rest_framework import serializers

from .models import CollectionPoint


class MapCollectionPointSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source="manager.get_full_name", read_only=True)

    class Meta:
        model = CollectionPoint
        fields = [
            "id",
            "name",
            "point_type",
            "status",
            "latitude",
            "longitude",
            "district",
            "neighborhood",
            "address",
            "accepts_plastic",
            "accepts_metal",
            "fill_level",
            "capacity_kg_day",
            "current_stock_kg",
            "plastic_price_kg",
            "metal_price_kg",
            "opening_days",
            "opening_time",
            "closing_time",
            "manager_name",
        ]

