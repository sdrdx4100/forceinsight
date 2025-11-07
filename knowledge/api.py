from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UsageLog, SavedSearch
from .serializers import UsageLogSerializer, SavedSearchSerializer


class UsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UsageLog.objects.select_related('user')
    serializer_class = UsageLogSerializer
    permission_classes = [IsAuthenticated]


class SavedSearchViewSet(viewsets.ModelViewSet):
    queryset = SavedSearch.objects.all()
    serializer_class = SavedSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
