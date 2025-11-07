import pandas as pd
import plotly.express as px
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datasets.models import MeasurementSet
from knowledge.utils import log_usage
from .models import SavedChart, Dashboard
from .serializers import SavedChartSerializer, DashboardSerializer


class SavedChartViewSet(viewsets.ModelViewSet):
    queryset = SavedChart.objects.select_related('user')
    serializer_class = SavedChartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chart = serializer.save(user=self.request.user)
        log_usage(self.request.user, action='save_chart', target=chart)


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.prefetch_related('charts', 'shared_with')
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlotlyPreviewView(generics.RetrieveAPIView):
    queryset = MeasurementSet.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        measurement_set = self.get_object()
        channel_maps = measurement_set.channel_maps.all()[:2]
        traces = []
        for channel_map in channel_maps:
            preview = channel_map.preview_ref
            df = pd.DataFrame(preview)
            df['channel'] = channel_map.channel_def.name
            traces.append(df)
        if not traces:
            return Response({'detail': 'プレビューが存在しません。'}, status=404)
        df = pd.concat(traces)
        fig = px.line(df, x='time', y='value', color='channel', title=measurement_set.title)
        html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        chart, _ = SavedChart.objects.get_or_create(
            user=request.user,
            name=f'Preview {measurement_set.id}',
            defaults={'snapshot_html': html, 'datasource_ref': {'measurement_set': measurement_set.id}}
        )
        chart.snapshot_html = html
        chart.save(update_fields=['snapshot_html'])
        log_usage(request.user, action='preview_chart', target=measurement_set, context={'channels': [cm.channel_def.name for cm in channel_maps]})
        return Response({'html': html})
