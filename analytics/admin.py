from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import SavedChart, Dashboard


@admin.register(SavedChart)
class SavedChartAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'updated_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('plot_preview',)

    def plot_preview(self, obj):
        if not obj.snapshot_html:
            return 'プレビューなし'
        return mark_safe(obj.snapshot_html)

    plot_preview.short_description = 'Plotly プレビュー'


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    filter_horizontal = ('shared_with', 'charts')
