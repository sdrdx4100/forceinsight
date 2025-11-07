from django import forms
from django.contrib import admin
from django.db import models

from .models import IngestionJob, FileMetadata


@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('path', 'format', 'size', 'checksum')
    search_fields = ('path', 'checksum', 'format')
    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': 6, 'class': 'vLargeTextField json-widget'})},
    }


@admin.register(IngestionJob)
class IngestionJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_metadata', 'measurement_set', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('file_metadata__path',)
    formfield_overrides = FileMetadataAdmin.formfield_overrides
