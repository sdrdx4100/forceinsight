from __future__ import annotations

import hashlib
from typing import Tuple

from django import forms

from datasets.models import MeasurementSet
from ingestion.models import FileMetadata, IngestionJob


class DataUploadForm(forms.Form):
    measurement_set = forms.ModelChoiceField(
        queryset=MeasurementSet.objects.none(),
        label='計測セット',
        help_text='アップロード対象の計測セットを選択してください。',
    )
    data_file = forms.FileField(label='データファイル')
    source = forms.CharField(label='取得元', max_length=128, required=False)
    format = forms.CharField(label='形式', max_length=32, initial='binary')
    notes = forms.CharField(label='メモ', required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['measurement_set'].queryset = (
            MeasurementSet.objects.select_related('vehicle').order_by('title')
        )
        self.fields['measurement_set'].label_from_instance = (
            lambda obj: f"{obj.title} / {obj.project} ({obj.vehicle.model_code})"
        )

    def save(self, user) -> Tuple[FileMetadata, IngestionJob]:
        uploaded = self.cleaned_data['data_file']
        checksum = hashlib.md5()
        size = 0
        for chunk in uploaded.chunks():
            size += len(chunk)
            checksum.update(chunk)
        uploaded.seek(0)

        notes = self.cleaned_data.get('notes') or ''
        metadata = FileMetadata.objects.create(
            path=uploaded.name,
            size=size,
            checksum=checksum.hexdigest(),
            source=self.cleaned_data.get('source', ''),
            format=self.cleaned_data['format'],
            meta={'notes': notes, 'original_name': uploaded.name},
        )
        metadata.uploaded_file.save(uploaded.name, uploaded, save=False)
        metadata.path = metadata.uploaded_file.name or metadata.path
        metadata.save()

        job = IngestionJob.objects.create(
            created_by=user if getattr(user, 'is_authenticated', False) else None,
            file_metadata=metadata,
            measurement_set=self.cleaned_data['measurement_set'],
            status='uploaded',
            report={'notes': notes} if notes else {},
        )
        return metadata, job
