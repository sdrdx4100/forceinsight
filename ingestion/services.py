"""取込ロジックをカプセル化したサービス層。"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import pandas as pd

from catalog.models import Vehicle
from datasets.models import ChannelDef, ChannelMap, MeasurementSet
from .models import FileMetadata, IngestionJob
from .parsers import ParsedChannel, select_parser

logger = logging.getLogger(__name__)


def downsample(samples: pd.DataFrame, limit: int = 200) -> pd.DataFrame:
    """プレビュー用にデータを間引く。"""
    if len(samples) <= limit:
        return samples
    return samples.iloc[:: max(len(samples) // limit, 1)].reset_index(drop=True)


def ingest_file(path: Path, *, project: str, vehicle: Vehicle, created_by, source: str = 'manual') -> MeasurementSet:
    parser = select_parser(path)
    parsed = parser.parse(path)

    checksum = parser.checksum(path)

    measurement_set = MeasurementSet.objects.create(
        title=path.stem,
        project=project,
        vehicle=vehicle,
        conditions={'parser': parser.__class__.__name__},
        file_refs={
            'path': str(path),
            'checksum': checksum,
            'format': path.suffix.lower(),
            'size': path.stat().st_size,
        },
        schema_version='1.0',
    )

    file_meta = FileMetadata.objects.create(
        path=str(path),
        size=path.stat().st_size,
        checksum=checksum,
        source=source,
        format=path.suffix.lower(),
        meta=parsed.metadata,
    )

    job = IngestionJob.objects.create(
        file_metadata=file_meta,
        measurement_set=measurement_set,
        status='completed',
        created_by=created_by,
        report={'channels': len(parsed.channels)},
    )

    _store_channels(parsed.channels, measurement_set)

    logger.info('取込完了: measurement_set=%s job=%s', measurement_set.id, job.id)
    return measurement_set


def _store_channels(channels: Iterable[ParsedChannel], measurement_set: MeasurementSet) -> None:
    for parsed_channel in channels:
        channel_def, _ = ChannelDef.objects.get_or_create(
            name=parsed_channel.name,
            defaults={
                'unit': parsed_channel.unit or '',
                'category': 'raw',
                'meta': {},
            }
        )
        preview_df = downsample(parsed_channel.samples)
        preview_ref = {
            'time': preview_df['time'].tolist(),
            'value': preview_df['value'].tolist(),
        }
        ChannelMap.objects.update_or_create(
            measurement_set=measurement_set,
            channel_def=channel_def,
            defaults={
                'stats': parsed_channel.stats,
                'preview_ref': preview_ref,
                'extra': {'unit': parsed_channel.unit},
            },
        )
