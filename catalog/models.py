from django.db import models


class Vehicle(models.Model):
    vin = models.CharField('VIN', max_length=32, blank=True, null=True, unique=True)
    model_code = models.CharField('モデルコード', max_length=64)
    year = models.PositiveIntegerField('年式', blank=True, null=True)
    powertrain = models.CharField('パワートレイン', max_length=64, blank=True, null=True)
    tags = models.JSONField('タグ', default=dict, blank=True)

    class Meta:
        verbose_name = '車両'
        verbose_name_plural = '車両'
        ordering = ['model_code', 'year']

    def __str__(self) -> str:
        return f"{self.model_code} ({self.year})"


class ECU(models.Model):
    name = models.CharField('ECU名称', max_length=128)
    firmware_version = models.CharField('ファームウェア', max_length=64, blank=True)
    meta = models.JSONField('メタ情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'ECU'
        verbose_name_plural = 'ECU'

    def __str__(self) -> str:
        return self.name


class Sensor(models.Model):
    name = models.CharField('センサー名', max_length=128)
    sensor_type = models.CharField('種類', max_length=64)
    unit = models.CharField('単位', max_length=32, blank=True)
    meta = models.JSONField('メタ情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'センサー'
        verbose_name_plural = 'センサー'

    def __str__(self) -> str:
        return self.name


class TestCourse(models.Model):
    name = models.CharField('試験コース', max_length=128)
    location = models.CharField('所在地', max_length=128, blank=True)
    environment = models.JSONField('環境情報', default=dict, blank=True)

    class Meta:
        verbose_name = 'テストコース'
        verbose_name_plural = 'テストコース'

    def __str__(self) -> str:
        return self.name
