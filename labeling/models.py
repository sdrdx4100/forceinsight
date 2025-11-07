from django.conf import settings
from django.db import models

from datasets.models import MeasurementSet, ChannelMap


class LabelSchema(models.Model):
    name = models.CharField('スキーマ名', max_length=128)
    tree_path = models.CharField('ツリー構造', max_length=512, help_text='ドット区切りで階層を定義します。')
    rules = models.JSONField('ルール', default=dict, blank=True)

    class Meta:
        verbose_name = 'ラベルスキーマ'
        verbose_name_plural = 'ラベルスキーマ'

    def __str__(self) -> str:
        return self.name


class Label(models.Model):
    schema = models.ForeignKey(LabelSchema, on_delete=models.CASCADE, related_name='labels')
    name = models.CharField('ラベル名', max_length=128)
    description = models.TextField('説明', blank=True)
    meta = models.JSONField('メタ情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'ラベル'
        verbose_name_plural = 'ラベル'

    def __str__(self) -> str:
        return f"{self.schema.name}:{self.name}"


class Annotation(models.Model):
    measurement_set = models.ForeignKey(MeasurementSet, on_delete=models.CASCADE, related_name='annotations', null=True, blank=True)
    channel_map = models.ForeignKey(ChannelMap, on_delete=models.CASCADE, related_name='annotations', null=True, blank=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='annotations')
    time_range = models.JSONField('時間範囲', default=dict, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField('ノート', blank=True)
    version = models.CharField('バージョン', max_length=32, default='1.0')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    class Meta:
        verbose_name = 'アノテーション'
        verbose_name_plural = 'アノテーション'
        ordering = ['-created_at']

    def __str__(self) -> str:
        target = self.channel_map or self.measurement_set
        return f"Annotation({target})"
