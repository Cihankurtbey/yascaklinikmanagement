from django.contrib import admin
from .models import Treatment, TreatmentType, Odontogram


@admin.register(TreatmentType)
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_price', 'color_code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'treatment_type', 'tooth_number', 'status', 'treatment_date')
    list_filter = ('status', 'treatment_type', 'treatment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'description')
    date_hierarchy = 'treatment_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Odontogram)
class OdontogramAdmin(admin.ModelAdmin):
    list_display = ('patient', 'updated_at')
    search_fields = ('patient__first_name', 'patient__last_name')
    readonly_fields = ('updated_at',)
