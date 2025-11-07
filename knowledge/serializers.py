from rest_framework import serializers

from .models import UsageLog, SavedSearch


class UsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageLog
        fields = ['id', 'user', 'action', 'target_id', 'target_type', 'context', 'at']
        read_only_fields = ['id', 'user', 'at']


class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = ['id', 'user', 'name', 'query', 'facets', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
