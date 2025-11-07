from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from catalog.models import Vehicle
from ingestion.services import ingest_file

User = get_user_model()


class Command(BaseCommand):
    help = 'サンプルの計測データ(擬似MDF)を生成し、取込処理を実行します。'

    def add_arguments(self, parser):
        parser.add_argument('--project', default='DemoProject')
        parser.add_argument('--vehicle', default='VX-01')

    def handle(self, *args: Any, **options: Any):
        project = options['project']
        vehicle_code = options['vehicle']
        vehicle, _ = Vehicle.objects.get_or_create(model_code=vehicle_code, defaults={'year': 2024})
        user = User.objects.first()
        if user is None:
            user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.WARNING('管理ユーザー admin/admin を自動生成しました。'))

        sample_path = self._create_sample_csv()
        measurement_set = ingest_file(sample_path, project=project, vehicle=vehicle, created_by=user)
        self.stdout.write(self.style.SUCCESS(f'取込完了: MeasurementSet ID={measurement_set.id}'))

    def _create_sample_csv(self) -> Path:
        base_dir = Path('tmp')
        base_dir.mkdir(exist_ok=True)
        path = base_dir / 'sample_dat.csv'
        times = [i * 0.1 for i in range(600)]
        speed = [30 + 5 * math.sin(i / 10) for i in range(600)]
        accel = [0.1 * math.cos(i / 15) for i in range(600)]
        df = pd.DataFrame({'time': times, 'speed': speed, 'accel': accel})
        df.to_csv(path, index=False)
        return path
