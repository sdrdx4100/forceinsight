from __future__ import annotations

from collections import Counter
import json
from typing import Any

from django import forms
from django.db.models import Count, Q

from datasets.models import MeasurementSet, ChannelMap


class MeasurementAdvancedSearchForm(forms.Form):
    project = forms.CharField(label='プロジェクト', required=False)
    vehicle = forms.CharField(label='車両型式', required=False)
    label = forms.CharField(label='ラベル', required=False)
    channel = forms.CharField(label='チャネル', required=False)
    period_from = forms.DateTimeField(label='計測日(開始)', required=False, input_formats=[
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
    ])
    period_to = forms.DateTimeField(label='計測日(終了)', required=False, input_formats=[
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
    ])
    text = forms.CharField(label='キーワード', required=False)

    facets: dict[str, Any]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facets = {}

    def has_filters(self) -> bool:
        return any(self.cleaned_data.get(field) for field in self.cleaned_data)

    def search(self) -> list[dict[str, Any]]:
        queryset = MeasurementSet.objects.select_related('vehicle')
        cleaned = self.cleaned_data

        if cleaned.get('project'):
            queryset = queryset.filter(project__icontains=cleaned['project'])
        if cleaned.get('vehicle'):
            queryset = queryset.filter(vehicle__model_code__icontains=cleaned['vehicle'])
        if cleaned.get('label'):
            queryset = queryset.filter(annotations__label__name__icontains=cleaned['label']).distinct()
        if cleaned.get('channel'):
            queryset = queryset.filter(channel_maps__channel_def__name__icontains=cleaned['channel']).distinct()
        if cleaned.get('period_from'):
            queryset = queryset.filter(run_at__gte=cleaned['period_from'])
        if cleaned.get('period_to'):
            queryset = queryset.filter(run_at__lte=cleaned['period_to'])
        if cleaned.get('text'):
            text = cleaned['text']
            queryset = queryset.filter(Q(title__icontains=text) | Q(conditions__icontains=text))

        self.facets = self._build_facets(queryset)

        return [
            {
                'id': ms.id,
                'title': ms.title,
                'project': ms.project,
                'vehicle': ms.vehicle.model_code,
                'run_at': ms.run_at,
                'conditions_text': json.dumps(ms.conditions, ensure_ascii=False, indent=2) if ms.conditions else '',
            }
            for ms in queryset[:100]
        ]

    def _build_facets(self, queryset):
        project_counts = queryset.values('project').annotate(count=Count('id')).order_by('-count')[:10]
        vehicle_counts = queryset.values('vehicle__model_code').annotate(count=Count('id')).order_by('-count')[:10]
        facets = {
            'project': [
                {'project': item['project'] or '未設定', 'count': item['count']} for item in project_counts
            ],
            'vehicle': [
                {
                    'vehicle__model_code': item['vehicle__model_code'] or '未設定',
                    'count': item['count'],
                }
                for item in vehicle_counts
            ],
        }
        channel_counts = Counter(
            ChannelMap.objects.filter(measurement_set__in=queryset).values_list('channel_def__category', flat=True)
        )
        facets['channel_category'] = [
            {'category': key or 'unknown', 'count': count}
            for key, count in channel_counts.items()
        ]
        return facets
