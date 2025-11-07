from rest_framework import serializers

from .models import FileMetadata, IngestionJob


class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = ['id', 'path', 'size', 'checksum', 'source', 'format', 'meta']


class IngestionJobSerializer(serializers.ModelSerializer):
    file_metadata = FileMetadataSerializer(read_only=True)
    file_metadata_id = serializers.PrimaryKeyRelatedField(
        queryset=FileMetadata.objects.all(),
        source='file_metadata',
        write_only=True
    )

    class Meta:
        model = IngestionJob
        fields = ['id', 'created_at', 'created_by', 'file_metadata', 'file_metadata_id', 'measurement_set', 'status', 'report']
        read_only_fields = ['id', 'created_at', 'created_by']
