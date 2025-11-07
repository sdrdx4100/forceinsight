"""asammdf を利用したMDF/MF4解析や dat ファイルのプラガブルパーサを提供するモジュール。"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd

try:
    from asammdf import MDF
except Exception:  # pragma: no cover - asammdf が無い環境ではスタブ扱い
    MDF = None  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class ParsedChannel:
    name: str
    unit: str | None
    samples: pd.DataFrame
    stats: Dict[str, float]


@dataclass
class ParsedMeasurement:
    metadata: Dict
    channels: List[ParsedChannel]


class BaseParser:
    """取込用パーサの抽象クラス。"""

    supported_formats: Iterable[str] = ()

    def supports(self, suffix: str) -> bool:
        return suffix.lower() in {fmt.lower() for fmt in self.supported_formats}

    def parse(self, path: Path) -> ParsedMeasurement:  # pragma: no cover - 抽象メソッド
        raise NotImplementedError

    def checksum(self, path: Path) -> str:
        hash_md5 = hashlib.md5()
        with path.open('rb') as fp:
            for chunk in iter(lambda: fp.read(8192), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


class MDFParser(BaseParser):
    supported_formats = {'.mdf', '.mf4'}

    def parse(self, path: Path) -> ParsedMeasurement:
        if MDF is None:
            raise RuntimeError('asammdf がインストールされていないため MDF 解析を実行できません。')

        logger.info('MDF/MF4 ファイルを解析しています: %s', path)
        mdf = MDF(str(path))
        meta = {
            'comment': mdf.comment,
            'version': getattr(mdf, 'version', None),
            'channels_count': len(mdf.channels_db),
        }
        channels: List[ParsedChannel] = []
        for name in mdf.channels_db:
            channel = mdf.get(name)
            series = channel.to_pandas()
            df = pd.DataFrame({'time': series.index.total_seconds(), 'value': series.values})
            stats = {
                'min': float(np.nanmin(series.values)),
                'max': float(np.nanmax(series.values)),
                'mean': float(np.nanmean(series.values)),
                'std': float(np.nanstd(series.values)),
                'count': int(series.count()),
            }
            channels.append(ParsedChannel(name=name, unit=channel.unit, samples=df, stats=stats))
        return ParsedMeasurement(metadata=meta, channels=channels)


class DummyDATParser(BaseParser):
    """dat ファイル向けの簡易スタブ実装。"""

    supported_formats = {'.dat'}

    def parse(self, path: Path) -> ParsedMeasurement:
        logger.info('DAT ファイル解析スタブを実行: %s', path)
        df = pd.read_csv(path)
        channels: List[ParsedChannel] = []
        for column in df.columns:
            if column == 'time':
                continue
            series = df[column]
            stats = {
                'min': float(series.min()),
                'max': float(series.max()),
                'mean': float(series.mean()),
                'std': float(series.std()),
                'count': int(series.count()),
            }
            channel_df = pd.DataFrame({'time': df['time'], 'value': series})
            channels.append(ParsedChannel(name=column, unit=None, samples=channel_df, stats=stats))
        meta = {'columns': list(df.columns)}
        return ParsedMeasurement(metadata=meta, channels=channels)


class CSVPreviewParser(DummyDATParser):
    """CSV (dat 互換) を読み込む簡易パーサ。"""

    supported_formats = {'.csv'}


DEFAULT_PARSERS: List[BaseParser] = [MDFParser(), DummyDATParser(), CSVPreviewParser()]


def select_parser(path: Path) -> BaseParser:
    suffix = path.suffix.lower()
    for parser in DEFAULT_PARSERS:
        if parser.supports(suffix):
            return parser
    raise ValueError(f'サポートされていないファイル形式です: {suffix}')
