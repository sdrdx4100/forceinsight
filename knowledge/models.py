from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class UsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usage_logs')
    action = models.CharField('操作', max_length=64)
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'target_id')
    context = models.JSONField('コンテキスト', default=dict, blank=True)
    at = models.DateTimeField('日時', auto_now_add=True)

    class Meta:
        verbose_name = '利用履歴'
        verbose_name_plural = '利用履歴'
        ordering = ['-at']

    def __str__(self) -> str:
        return f"{self.user} {self.action} {self.target}"


class SavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField('名称', max_length=128)
    query = models.JSONField('クエリ', default=dict, blank=True)
    facets = models.JSONField('ファセット', default=dict, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '保存済み検索'
        verbose_name_plural = '保存済み検索'
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return self.name
