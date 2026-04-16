from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.collection_points.models import CollectionPoint
from apps.collection_points.serializers import MapCollectionPointSerializer


class MapPointsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = CollectionPoint.objects.filter(status="active").order_by("name")
        serializer = MapCollectionPointSerializer(queryset, many=True)
        return Response(serializer.data)

