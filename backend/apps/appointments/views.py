from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, AppointmentSettings
from .serializers import (
    AppointmentSerializer,
    AppointmentListSerializer,
    AppointmentCreateSerializer,
    AppointmentSettingsSerializer
)
from apps.users.permissions import IsAssistantOrAbove, IsAdminOrReadOnly


class AppointmentViewSet(viewsets.ModelViewSet):
    """Appointment ViewSet"""
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated, IsAssistantOrAbove]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__phone', 'procedure']
    ordering_fields = ['appointment_date', 'appointment_time', 'created_at']
    ordering = ['appointment_date', 'appointment_time']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        elif self.action == 'list':
            return AppointmentListSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtreler
        date = self.request.query_params.get('date', None)
        doctor = self.request.query_params.get('doctor', None)
        status_filter = self.request.query_params.get('status', None)
        
        if date:
            queryset = queryset.filter(appointment_date=date)
        
        if doctor:
            queryset = queryset.filter(doctor_id=doctor)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Bugünün randevuları
        today = self.request.query_params.get('today', None)
        if today == 'true':
            queryset = queryset.filter(appointment_date=timezone.now().date())
        
        return queryset
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Randevu durumunu güncelle (F-009)"""
        appointment = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in [choice[0] for choice in Appointment.AppointmentStatus.choices]:
            return Response(
                {'error': 'Geçersiz durum.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = new_status
        appointment.save()
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Takvim görünümü için randevuları getir (F-006)"""
        view_type = request.query_params.get('view', 'daily')  # daily, weekly, monthly
        date_str = request.query_params.get('date', None)
        doctor_id = request.query_params.get('doctor', None)
        
        if date_str:
            try:
                start_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except:
                start_date = timezone.now().date()
        else:
            start_date = timezone.now().date()
        
        queryset = self.get_queryset()
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        if view_type == 'daily':
            queryset = queryset.filter(appointment_date=start_date)
        elif view_type == 'weekly':
            end_date = start_date + timedelta(days=6)
            queryset = queryset.filter(
                appointment_date__gte=start_date,
                appointment_date__lte=end_date
            )
        elif view_type == 'monthly':
            # Ayın ilk ve son günü
            from calendar import monthrange
            last_day = monthrange(start_date.year, start_date.month)[1]
            end_date = start_date.replace(day=last_day)
            queryset = queryset.filter(
                appointment_date__gte=start_date.replace(day=1),
                appointment_date__lte=end_date
            )
        
        serializer = AppointmentListSerializer(queryset, many=True)
        return Response(serializer.data)


class AppointmentSettingsViewSet(viewsets.ModelViewSet):
    """Appointment Settings ViewSet (F-022)"""
    queryset = AppointmentSettings.objects.all()
    serializer_class = AppointmentSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_object(self):
        return AppointmentSettings.get_settings()
    
    def list(self, request, *args, **kwargs):
        """Tek bir ayar kaydı olduğu için list yerine retrieve"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Ayar kaydı oluştur"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Ayar kaydını güncelle"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)
