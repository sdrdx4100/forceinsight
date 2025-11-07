from rest_framework import serializers

from .models import LabelSchema, Label, Annotation


class LabelSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelSchema
        fields = ['id', 'name', 'tree_path', 'rules']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'schema', 'name', 'description', 'meta']


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'measurement_set', 'channel_map', 'label', 'time_range', 'author', 'note', 'version', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
