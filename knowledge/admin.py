from django import forms
from django.contrib import admin
from django.db import models

from .models import UsageLog, SavedSearch


@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'target', 'at')
    list_filter = ('action', 'at')
    search_fields = ('user__username', 'action', 'target_id')
    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': 6, 'class': 'vLargeTextField json-widget'})},
    }


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'updated_at')
    search_fields = ('name', 'user__username')
    formfield_overrides = UsageLogAdmin.formfield_overrides
