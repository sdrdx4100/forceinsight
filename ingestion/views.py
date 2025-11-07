from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from ingestion.forms import DataUploadForm
from ingestion.models import IngestionJob


class DataUploadView(LoginRequiredMixin, FormView):
    form_class = DataUploadForm
    template_name = 'ingestion/data_upload.html'
    success_url = reverse_lazy('data-upload')

    def form_valid(self, form):
        metadata, job = form.save(self.request.user)
        messages.success(
            self.request,
            (
                f'ファイル「{metadata.meta.get("original_name", metadata.path)}」をアップロードし、'
                f'ジョブ #{job.pk} を作成しました。'
            ),
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_jobs'] = (
            IngestionJob.objects.select_related('file_metadata', 'measurement_set')
            .order_by('-created_at')[:10]
        )
        return context
