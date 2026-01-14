from rest_framework import serializers
from .models import Treatment, TreatmentType, Odontogram
from apps.patients.serializers import PatientListSerializer
from apps.users.serializers import UserSerializer


class TreatmentTypeSerializer(serializers.ModelSerializer):
    """Treatment Type Serializer"""
    
    class Meta:
        model = TreatmentType
        fields = ('id', 'name', 'default_price', 'color_code', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class TreatmentSerializer(serializers.ModelSerializer):
    """Treatment Serializer"""
    patient_detail = PatientListSerializer(source='patient', read_only=True)
    doctor_detail = UserSerializer(source='doctor', read_only=True)
    treatment_type_detail = TreatmentTypeSerializer(source='treatment_type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Treatment
        fields = (
            'id', 'patient', 'patient_detail', 'doctor', 'doctor_detail',
            'treatment_type', 'treatment_type_detail', 'tooth_number',
            'is_primary_tooth', 'description', 'status', 'status_display',
            'treatment_date', 'price', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class TreatmentListSerializer(serializers.ModelSerializer):
    """Treatment List Serializer (lightweight)"""
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    treatment_type_name = serializers.CharField(source='treatment_type.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Treatment
        fields = (
            'id', 'patient_name', 'doctor_name', 'treatment_type_name',
            'tooth_number', 'description', 'status', 'status_display',
            'treatment_date'
        )


class OdontogramSerializer(serializers.ModelSerializer):
    """Odontogram Serializer"""
    patient_detail = PatientListSerializer(source='patient', read_only=True)
    
    class Meta:
        model = Odontogram
        fields = ('id', 'patient', 'patient_detail', 'permanent_teeth', 'primary_teeth', 'updated_at')
        read_only_fields = ('id', 'updated_at')
