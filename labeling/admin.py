from django import forms
from django.contrib import admin
from django.db import models

from .models import LabelSchema, Label, Annotation


@admin.register(LabelSchema)
class LabelSchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'tree_path')
    search_fields = ('name', 'tree_path')
    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': 6, 'class': 'vLargeTextField json-widget'})},
    }


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema')
    list_filter = ('schema',)
    search_fields = ('name',)
    formfield_overrides = LabelSchemaAdmin.formfield_overrides


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('label', 'measurement_set', 'channel_map', 'author', 'created_at')
    list_filter = ('label', 'author', 'created_at')
    search_fields = ('note',)
    formfield_overrides = LabelSchemaAdmin.formfield_overrides
