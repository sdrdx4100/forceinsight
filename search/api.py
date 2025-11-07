from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any

from django.db.models import Count, Q
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datasets.models import MeasurementSet, ChannelMap
from knowledge.utils import log_usage


class MeasurementSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = MeasurementSet.objects.select_related('vehicle')
        params = request.query_params

        if project := params.get('project'):
            queryset = queryset.filter(project__icontains=project)
        if vehicle := params.get('vehicle'):
            queryset = queryset.filter(vehicle__model_code__icontains=vehicle)
        if label := params.get('label'):
            queryset = queryset.filter(annotations__label__name__icontains=label).distinct()
        if channel := params.get('channel'):
            queryset = queryset.filter(channel_maps__channel_def__name__icontains=channel).distinct()
        if period_from := params.get('from'):
            parsed = parse_datetime(period_from)
            if parsed:
                queryset = queryset.filter(run_at__gte=parsed)
        if period_to := params.get('to'):
            parsed = parse_datetime(period_to)
            if parsed:
                queryset = queryset.filter(run_at__lte=parsed)
        if text := params.get('text'):
            queryset = queryset.filter(Q(title__icontains=text) | Q(conditions__icontains=text))

        results = [
            {
                'id': ms.id,
                'title': ms.title,
                'project': ms.project,
                'vehicle': ms.vehicle.model_code,
                'run_at': ms.run_at,
                'conditions': ms.conditions,
            }
            for ms in queryset[:50]
        ]

        facets = self._build_facets(queryset)
        first = queryset.first()
        if first:
            log_usage(request.user, action='search_measurement', target=first, context={'count': queryset.count(), 'params': params})
        return Response({'results': results, 'facets': facets})

    def _build_facets(self, queryset):
        facets = {
            'project': list(queryset.values('project').annotate(count=Count('id')).order_by('-count')[:10]),
            'vehicle': list(queryset.values('vehicle__model_code').annotate(count=Count('id')).order_by('-count')[:10]),
        }
        channel_counts = Counter(
            ChannelMap.objects.filter(measurement_set__in=queryset).values_list('channel_def__category', flat=True)
        )
        facets['channel_category'] = [{'category': key or 'unknown', 'count': count} for key, count in channel_counts.items()]
        return facets
