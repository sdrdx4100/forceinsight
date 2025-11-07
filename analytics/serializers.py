from rest_framework import serializers

from .models import SavedChart, Dashboard


class SavedChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedChart
        fields = ['id', 'user', 'name', 'spec', 'datasource_ref', 'snapshot_html', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ['id', 'title', 'layout', 'owner', 'shared_with', 'charts']
        read_only_fields = ['id', 'owner']
