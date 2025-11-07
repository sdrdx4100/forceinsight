import pandas as pd
import plotly.express as px
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from datasets.models import MeasurementSet
from knowledge.utils import log_usage


class MeasurementPlotView(LoginRequiredMixin, DetailView):
    model = MeasurementSet
    template_name = 'analytics/chart_detail.html'
    context_object_name = 'measurement_set'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_maps = self.object.channel_maps.all()[:2]
        traces = []
        channel_names = []
        for channel_map in channel_maps:
            preview = channel_map.preview_ref
            if not preview:
                continue
            df = pd.DataFrame(preview)
            df['channel'] = channel_map.channel_def.name
            channel_names.append(channel_map.channel_def.name)
            traces.append(df)
        if traces:
            df = pd.concat(traces)
            fig = px.line(df, x='time', y='value', color='channel', title=self.object.title)
            context['plot_html'] = fig.to_html(full_html=False, include_plotlyjs='cdn')
        else:
            context['plot_html'] = '<p>プレビューなし</p>'
        context['channel_names'] = channel_names
        log_usage(self.request.user, action='view_chart', target=self.object, context={'channels': channel_names})
        return context
