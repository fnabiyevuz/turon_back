from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.common import serializers as com_ser
from apps.common.models import Region, District, Neighborhood, Media


class RegionListView(ListAPIView):
    queryset = Region.objects.all().order_by('name')
    serializer_class = com_ser.RegionListSerializer
    search_fields = ('name',)


class DistrictListView(ListAPIView):
    queryset = District.objects.all().order_by('name')
    serializer_class = com_ser.DistrictListSerializer
    filterset_fields = ("region",)
    search_fields = ('name',)


class NeighborhoodListView(ListAPIView):
    queryset = Neighborhood.objects.all().order_by('name')
    serializer_class = com_ser.NeighborhoodListSerializer
    filterset_fields = ("district",)
    search_fields = ('name',)


class MediaCreateAPIView(CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = com_ser.MediaSerializer
    parser_classes = (MultiPartParser, FormParser)
