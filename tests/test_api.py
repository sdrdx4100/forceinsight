import pandas as pd
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ingestion.services import ingest_file


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.mark.django_db
def test_measurement_set_api_list(api_client, user, vehicle, tmp_path):
    path = tmp_path / 'sample.csv'
    df = pd.DataFrame({'time': [0, 1, 2], 'speed': [10, 20, 30]})
    df.to_csv(path, index=False)
    ingest_file(path, project='API', vehicle=vehicle, created_by=user)

    url = reverse('measurementset-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['results'][0]['project'] == 'API'


@pytest.mark.django_db
def test_plotly_preview_api(api_client, user, vehicle, tmp_path):
    path = tmp_path / 'sample.csv'
    df = pd.DataFrame({'time': [0, 1, 2], 'speed': [10, 20, 30]})
    df.to_csv(path, index=False)
    measurement_set = ingest_file(path, project='API', vehicle=vehicle, created_by=user)

    url = reverse('plotly-preview', args=[measurement_set.pk])
    response = api_client.get(url)
    assert response.status_code == 200
    assert '<div' in response.data['html']


@pytest.mark.django_db
def test_measurement_search(api_client, user, vehicle, tmp_path):
    path = tmp_path / 'sample.csv'
    df = pd.DataFrame({'time': [0, 1, 2], 'speed': [10, 20, 30]})
    df.to_csv(path, index=False)
    ingest_file(path, project='Search', vehicle=vehicle, created_by=user)

    url = reverse('measurement-search')
    response = api_client.get(url, {'project': 'Search'})
    assert response.status_code == 200
    assert len(response.data['results']) == 1
