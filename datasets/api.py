from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import MeasurementSet, ChannelDef, ChannelMap
from .serializers import MeasurementSetSerializer, ChannelDefSerializer, ChannelMapSerializer


class MeasurementSetViewSet(viewsets.ModelViewSet):
    queryset = MeasurementSet.objects.all().select_related('vehicle')
    serializer_class = MeasurementSetSerializer
    permission_classes = [IsAuthenticated]


class ChannelDefViewSet(viewsets.ModelViewSet):
    queryset = ChannelDef.objects.all()
    serializer_class = ChannelDefSerializer
    permission_classes = [IsAuthenticated]


class ChannelMapViewSet(viewsets.ModelViewSet):
    queryset = ChannelMap.objects.all().select_related('measurement_set', 'channel_def')
    serializer_class = ChannelMapSerializer
    permission_classes = [IsAuthenticated]
