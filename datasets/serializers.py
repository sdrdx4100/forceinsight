from rest_framework import serializers

from .models import ChannelDef, ChannelMap, MeasurementSet


class ChannelDefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelDef
        fields = ['id', 'name', 'unit', 'rate_hz', 'category', 'meta']


class ChannelMapSerializer(serializers.ModelSerializer):
    channel_def = ChannelDefSerializer(read_only=True)
    channel_def_id = serializers.PrimaryKeyRelatedField(
        queryset=ChannelDef.objects.all(),
        source='channel_def',
        write_only=True
    )

    class Meta:
        model = ChannelMap
        fields = ['id', 'measurement_set', 'channel_def', 'channel_def_id', 'stats', 'preview_ref', 'extra']
        read_only_fields = ['id']


class MeasurementSetSerializer(serializers.ModelSerializer):
    vehicle_display = serializers.CharField(source='vehicle.model_code', read_only=True)
    channel_maps = ChannelMapSerializer(many=True, read_only=True)

    class Meta:
        model = MeasurementSet
        fields = [
            'id', 'title', 'project', 'vehicle', 'vehicle_display',
            'run_at', 'conditions', 'file_refs', 'schema_version', 'channel_maps'
        ]
        read_only_fields = ['id']
