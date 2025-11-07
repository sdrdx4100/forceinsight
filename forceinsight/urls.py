from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from analytics.api import SavedChartViewSet, DashboardViewSet, PlotlyPreviewView
from analytics.views import MeasurementPlotView
from catalog.api import VehicleViewSet
from datasets.api import MeasurementSetViewSet, ChannelDefViewSet, ChannelMapViewSet
from ingestion.api import IngestionJobViewSet, FileMetadataViewSet
from ingestion.views import DataUploadView
from knowledge.api import UsageLogViewSet, SavedSearchViewSet
from labeling.api import LabelSchemaViewSet, LabelViewSet, AnnotationViewSet
from search.api import MeasurementSearchView
from search.views import AdvancedMeasurementSearchView
from accounts.api import UserViewSet
from ops.views import HealthCheckView
from export.views import MeasurementCSVExportView

router = routers.DefaultRouter()
router.register(r'accounts/users', UserViewSet)
router.register(r'catalog/vehicles', VehicleViewSet)
router.register(r'datasets/measurement-sets', MeasurementSetViewSet)
router.register(r'datasets/channel-defs', ChannelDefViewSet)
router.register(r'datasets/channel-maps', ChannelMapViewSet)
router.register(r'ingestion/jobs', IngestionJobViewSet)
router.register(r'ingestion/files', FileMetadataViewSet)
router.register(r'labeling/schemas', LabelSchemaViewSet)
router.register(r'labeling/labels', LabelViewSet)
router.register(r'labeling/annotations', AnnotationViewSet)
router.register(r'knowledge/usage-log', UsageLogViewSet)
router.register(r'knowledge/saved-searches', SavedSearchViewSet)
router.register(r'analytics/saved-charts', SavedChartViewSet)
router.register(r'analytics/dashboards', DashboardViewSet)

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/search/measurement-sets/', MeasurementSearchView.as_view(), name='measurement-search'),
    path('api/plotly/preview/<int:pk>/', PlotlyPreviewView.as_view(), name='plotly-preview'),
    path('api/', include(router.urls)),
    path('visualizations/measurement/<int:pk>/', MeasurementPlotView.as_view(), name='measurement-plot'),
    path('export/measurement/<int:pk>/csv/', MeasurementCSVExportView.as_view(), name='measurement-export-csv'),
    path('ingestion/upload/', DataUploadView.as_view(), name='data-upload'),
    path('search/advanced/', AdvancedMeasurementSearchView.as_view(), name='advanced-search'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
