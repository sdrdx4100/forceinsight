from django.db import models
from django.utils import timezone

from catalog.models import Vehicle


class MeasurementSet(models.Model):
    title = models.CharField('タイトル', max_length=255)
    project = models.CharField('プロジェクト', max_length=128)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='measurement_sets')
    run_at = models.DateTimeField('計測日時', default=timezone.now)
    conditions = models.JSONField('計測条件', default=dict, blank=True)
    file_refs = models.JSONField('ファイル参照', default=dict, blank=True)
    schema_version = models.CharField('スキーマバージョン', max_length=32, default='1.0')

    class Meta:
        verbose_name = '計測データセット'
        verbose_name_plural = '計測データセット'
        ordering = ['-run_at']

    def __str__(self) -> str:
        return f"{self.title} ({self.project})"


class ChannelDef(models.Model):
    name = models.CharField('チャネル名', max_length=255)
    unit = models.CharField('単位', max_length=32, blank=True)
    rate_hz = models.FloatField('サンプリング周波数(Hz)', blank=True, null=True)
    category = models.CharField('カテゴリ', max_length=64, blank=True)
    meta = models.JSONField('メタ情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'チャネル定義'
        verbose_name_plural = 'チャネル定義'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ChannelMap(models.Model):
    measurement_set = models.ForeignKey(MeasurementSet, on_delete=models.CASCADE, related_name='channel_maps')
    channel_def = models.ForeignKey(ChannelDef, on_delete=models.CASCADE, related_name='channel_maps')
    stats = models.JSONField('統計情報', default=dict, blank=True)
    preview_ref = models.JSONField('プレビュー参照', default=dict, blank=True)
    extra = models.JSONField('追加情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'チャネルマッピング'
        verbose_name_plural = 'チャネルマッピング'
        unique_together = ('measurement_set', 'channel_def')

    def __str__(self) -> str:
        return f"{self.measurement_set} - {self.channel_def}"
