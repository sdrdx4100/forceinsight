import csv

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from datasets.models import MeasurementSet


class MeasurementCSVExportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        measurement_set = MeasurementSet.objects.get(pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="measurement_{pk}.csv"'
        writer = csv.writer(response)
        writer.writerow(['channel', 'time', 'value'])
        for channel_map in measurement_set.channel_maps.all():
            preview = channel_map.preview_ref
            for time, value in zip(preview.get('time', []), preview.get('value', [])):
                writer.writerow([channel_map.channel_def.name, time, value])
        return response
