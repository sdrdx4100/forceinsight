from pathlib import Path

import pandas as pd
import pytest

from ingestion.services import ingest_file


@pytest.mark.django_db
def test_ingest_file_creates_measurement_set(user, vehicle, tmp_path):
    path = tmp_path / 'sample.csv'
    df = pd.DataFrame({'time': [0, 1, 2], 'speed': [10, 20, 30], 'accel': [0.1, 0.2, 0.3]})
    df.to_csv(path, index=False)

    measurement_set = ingest_file(path, project='TestProject', vehicle=vehicle, created_by=user)

    assert measurement_set.channel_maps.count() == 2
    channel_map = measurement_set.channel_maps.first()
    assert 'time' in channel_map.preview_ref
    assert channel_map.stats['count'] == 3
