from django.conf import settings
from django.db import models
from django.utils import timezone

from datasets.models import MeasurementSet


class FileMetadata(models.Model):
    path = models.CharField('ファイルパス', max_length=512)
    uploaded_file = models.FileField('アップロードファイル', upload_to='uploads/', blank=True, null=True)
    size = models.BigIntegerField('ファイルサイズ', default=0)
    checksum = models.CharField('ハッシュ', max_length=128)
    source = models.CharField('取得元', max_length=128, blank=True)
    format = models.CharField('形式', max_length=32)
    meta = models.JSONField('メタ情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'ファイルメタ情報'
        verbose_name_plural = 'ファイルメタ情報'

    def __str__(self) -> str:
        return f"{self.path} ({self.format})"


class IngestionJob(models.Model):
    created_at = models.DateTimeField('作成日時', default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    file_metadata = models.ForeignKey(FileMetadata, on_delete=models.CASCADE, related_name='ingestion_jobs')
    measurement_set = models.ForeignKey(MeasurementSet, on_delete=models.CASCADE, related_name='ingestion_jobs')
    status = models.CharField('ステータス', max_length=32, default='pending')
    report = models.JSONField('レポート', default=dict, blank=True)

    class Meta:
        verbose_name = '取込ジョブ'
        verbose_name_plural = '取込ジョブ'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Job#{self.pk} {self.file_metadata.path}"
