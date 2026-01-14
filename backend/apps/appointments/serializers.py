from rest_framework import serializers
from .models import Appointment, AppointmentSettings
from apps.patients.serializers import PatientListSerializer
from apps.users.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment Serializer"""
    patient_detail = PatientListSerializer(source='patient', read_only=True)
    doctor_detail = UserSerializer(source='doctor', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = (
            'id', 'patient', 'patient_detail', 'doctor', 'doctor_detail',
            'appointment_date', 'appointment_time', 'procedure', 'notes',
            'status', 'status_display', 'created_by_name',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate(self, attrs):
        """Randevu çakışmasını kontrol et"""
        doctor = attrs.get('doctor', self.instance.doctor if self.instance else None)
        appointment_date = attrs.get('appointment_date', self.instance.appointment_date if self.instance else None)
        appointment_time = attrs.get('appointment_time', self.instance.appointment_time if self.instance else None)
        
        if doctor and appointment_date and appointment_time:
            conflicting = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'completed']
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if conflicting.exists():
                raise serializers.ValidationError(
                    'Bu saatte doktora zaten bir randevu kayıtlı. Lütfen farklı bir saat seçin.'
                )
        
        return attrs


class AppointmentListSerializer(serializers.ModelSerializer):
    """Appointment List Serializer (lightweight)"""
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = (
            'id', 'patient_name', 'doctor_name', 'appointment_date',
            'appointment_time', 'procedure', 'status', 'status_display'
        )


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Appointment Create Serializer"""
    
    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'appointment_date', 'appointment_time',
                  'procedure', 'notes', 'status')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class AppointmentSettingsSerializer(serializers.ModelSerializer):
    """Appointment Settings Serializer"""
    
    class Meta:
        model = AppointmentSettings
        fields = ('id', 'start_time', 'end_time', 'slot_duration', 'updated_at')
        read_only_fields = ('id', 'updated_at')
