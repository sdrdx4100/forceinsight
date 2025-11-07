from django.conf import settings
from django.db import models


class SavedChart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_charts')
    name = models.CharField('名称', max_length=128)
    spec = models.JSONField('チャート仕様', default=dict, blank=True)
    datasource_ref = models.JSONField('データソース参照', default=dict, blank=True)
    snapshot_html = models.TextField('Plotly HTML', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '保存済みチャート'
        verbose_name_plural = '保存済みチャート'
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return self.name


class Dashboard(models.Model):
    title = models.CharField('タイトル', max_length=128)
    layout = models.JSONField('レイアウト', default=dict, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboards')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_dashboards', blank=True)
    charts = models.ManyToManyField(SavedChart, related_name='dashboards', blank=True)

    class Meta:
        verbose_name = 'ダッシュボード'
        verbose_name_plural = 'ダッシュボード'

    def __str__(self) -> str:
        return self.title
