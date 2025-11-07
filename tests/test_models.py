import pytest

from analytics.models import SavedChart
from knowledge.utils import log_usage


@pytest.mark.django_db
def test_saved_chart_str(user):
    chart = SavedChart.objects.create(user=user, name='Test Chart')
    assert str(chart) == 'Test Chart'


@pytest.mark.django_db
def test_log_usage(user, vehicle):
    chart = SavedChart.objects.create(user=user, name='Log Chart')
    log = log_usage(user, action='preview', target=chart, context={'foo': 'bar'})
    assert log.action == 'preview'
    assert log.context['foo'] == 'bar'
