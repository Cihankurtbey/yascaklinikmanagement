from django.contrib import admin
from .models import Appointment, AppointmentSettings


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'procedure')
    date_hierarchy = 'appointment_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AppointmentSettings)
class AppointmentSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'slot_duration', 'updated_at')
    readonly_fields = ('updated_at',)
