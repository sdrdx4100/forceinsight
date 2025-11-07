from django import forms
from django.contrib import admin
from django.db import models

from .models import MeasurementSet, ChannelDef, ChannelMap


@admin.register(MeasurementSet)
class MeasurementSetAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'vehicle', 'run_at')
    search_fields = ('title', 'project', 'vehicle__model_code')
    list_filter = ('project', 'vehicle__model_code', 'run_at')
    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': 6, 'class': 'vLargeTextField json-widget'})},
    }


@admin.register(ChannelDef)
class ChannelDefAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'rate_hz', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    formfield_overrides = MeasurementSetAdmin.formfield_overrides


@admin.register(ChannelMap)
class ChannelMapAdmin(admin.ModelAdmin):
    list_display = ('measurement_set', 'channel_def')
    search_fields = ('measurement_set__title', 'channel_def__name')
    formfield_overrides = MeasurementSetAdmin.formfield_overrides
