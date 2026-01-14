from rest_framework import serializers
from .models import Notification
from apps.appointments.serializers import AppointmentListSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Notification Serializer"""
    appointment_detail = AppointmentListSerializer(source='appointment', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = (
            'id', 'appointment', 'appointment_detail',
            'notification_type', 'notification_type_display',
            'message', 'recipient_phone', 'status', 'status_display',
            'sent_at', 'error_message', 'created_at'
        )
        read_only_fields = ('id', 'created_at', 'sent_at')
