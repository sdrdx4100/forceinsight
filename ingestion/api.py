from pathlib import Path

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from catalog.models import Vehicle
from .models import FileMetadata, IngestionJob
from .serializers import FileMetadataSerializer, IngestionJobSerializer
from .services import ingest_file


class FileMetadataViewSet(viewsets.ModelViewSet):
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer
    permission_classes = [IsAuthenticated]


class IngestionJobViewSet(viewsets.ModelViewSet):
    queryset = IngestionJob.objects.select_related('file_metadata', 'measurement_set')
    serializer_class = IngestionJobSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='ingest-path')
    def ingest_path(self, request):
        """ローカルファイルパスを指定して同期取込を行う簡易API。"""
        path = Path(request.data.get('path'))
        vehicle_id = request.data.get('vehicle_id')
        project = request.data.get('project', 'default')
        if not path.exists():
            return Response({'detail': '指定されたパスが存在しません。'}, status=status.HTTP_400_BAD_REQUEST)
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        measurement_set = ingest_file(path, project=project, vehicle=vehicle, created_by=request.user)
        serializer = IngestionJobSerializer(self.get_queryset().filter(measurement_set=measurement_set).last())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
