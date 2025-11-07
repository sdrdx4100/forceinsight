from django import forms
from django.contrib import admin
from django.db import models

from .models import Vehicle, ECU, Sensor, TestCourse


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model_code', 'year', 'powertrain', 'vin')
    search_fields = ('model_code', 'vin', 'powertrain')
    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': 6, 'class': 'vLargeTextField json-widget'})},
    }


@admin.register(ECU)
class ECUAdmin(admin.ModelAdmin):
    list_display = ('name', 'firmware_version')
    formfield_overrides = VehicleAdmin.formfield_overrides


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sensor_type', 'unit')
    search_fields = ('name', 'sensor_type')
    formfield_overrides = VehicleAdmin.formfield_overrides


@admin.register(TestCourse)
class TestCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    formfield_overrides = VehicleAdmin.formfield_overrides
