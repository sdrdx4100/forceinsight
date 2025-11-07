from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from search.forms import MeasurementAdvancedSearchForm


class AdvancedMeasurementSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search/advanced_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MeasurementAdvancedSearchForm(self.request.GET or None)
        results = []
        if form.is_valid() and (self.request.GET and form.has_filters()):
            results = form.search()
        context['form'] = form
        context['results'] = results
        context['facets'] = form.facets
        context['result_count'] = len(results)
        return context
