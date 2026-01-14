from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Treatment, TreatmentType, Odontogram
from .serializers import (
    TreatmentSerializer,
    TreatmentListSerializer,
    TreatmentTypeSerializer,
    OdontogramSerializer
)
from apps.users.permissions import IsDoctorOrAdmin, IsAdminOrReadOnly


class TreatmentTypeViewSet(viewsets.ModelViewSet):
    """Treatment Type ViewSet (F-020)"""
    queryset = TreatmentType.objects.filter(is_active=True)
    serializer_class = TreatmentTypeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]


class TreatmentViewSet(viewsets.ModelViewSet):
    """Treatment ViewSet"""
    queryset = Treatment.objects.all()
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'description']
    ordering_fields = ['treatment_date', 'created_at']
    ordering = ['-treatment_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TreatmentListSerializer
        return TreatmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtreler
        patient_id = self.request.query_params.get('patient', None)
        status_filter = self.request.query_params.get('status', None)
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class OdontogramViewSet(viewsets.ModelViewSet):
    """Odontogram ViewSet"""
    queryset = Odontogram.objects.all()
    serializer_class = OdontogramSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Hasta ID'ye göre filtrele
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset
    
    @action(detail=False, methods=['get', 'post'])
    def by_patient(self, request):
        """Hastaya göre odontogram getir veya oluştur"""
        patient_id = request.query_params.get('patient_id') or request.data.get('patient_id')
        
        if not patient_id:
            return Response(
                {'error': 'patient_id gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        odontogram, created = Odontogram.objects.get_or_create(patient_id=patient_id)
        serializer = OdontogramSerializer(odontogram)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_tooth(self, request, pk=None):
        """Diş durumunu güncelle (F-011)"""
        odontogram = self.get_object()
        tooth_number = request.data.get('tooth_number')
        is_primary = request.data.get('is_primary', False)
        treatment_data = request.data.get('treatment_data', {})
        
        if not tooth_number:
            return Response(
                {'error': 'tooth_number gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        teeth_data = odontogram.primary_teeth if is_primary else odontogram.permanent_teeth
        
        if tooth_number not in teeth_data:
            teeth_data[tooth_number] = []
        
        teeth_data[tooth_number].append(treatment_data)
        
        if is_primary:
            odontogram.primary_teeth = teeth_data
        else:
            odontogram.permanent_teeth = teeth_data
        
        odontogram.save()
        
        serializer = OdontogramSerializer(odontogram)
        return Response(serializer.data)
