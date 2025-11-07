from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import LabelSchema, Label, Annotation
from .serializers import LabelSchemaSerializer, LabelSerializer, AnnotationSerializer


class LabelSchemaViewSet(viewsets.ModelViewSet):
    queryset = LabelSchema.objects.all()
    serializer_class = LabelSchemaSerializer
    permission_classes = [IsAuthenticated]


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.select_related('schema')
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.select_related('label', 'measurement_set', 'channel_map')
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
