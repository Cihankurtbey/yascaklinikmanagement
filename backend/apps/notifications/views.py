from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from .services import NotificationService
from apps.appointments.models import Appointment
from apps.users.permissions import IsAssistantOrAbove


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """Notification ViewSet"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAssistantOrAbove]
    
    @action(detail=False, methods=['post'])
    def send_appointment_notification(self, request):
        """Randevu bildirimi gönder"""
        appointment_id = request.data.get('appointment_id')
        
        if not appointment_id:
            return Response(
                {'error': 'appointment_id gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            notification = NotificationService.send_appointment_notification(appointment)
            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Randevu bulunamadı'},
                status=status.HTTP_404_NOT_FOUND
            )
