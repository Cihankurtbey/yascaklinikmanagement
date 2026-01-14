from django.contrib import admin
from .models import Patient, PatientAnamnesis, PatientDocument


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'last_visit', 'created_at')
    list_filter = ('created_at', 'last_visit')
    search_fields = ('first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PatientAnamnesis)
class PatientAnamnesisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'updated_at')
    search_fields = ('patient__first_name', 'patient__last_name')


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'title', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'title')
