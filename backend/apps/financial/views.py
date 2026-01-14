from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from .models import Payment, PriceList
from .serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PriceListSerializer
)
from apps.patients.models import Patient
from apps.users.permissions import IsAssistantOrAbove, IsAdminOrReadOnly


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment ViewSet"""
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsAssistantOrAbove]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Hasta ID'ye göre filtrele
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def patient_balance(self, request):
        """Hastanın finansal durumunu getir (F-015)"""
        patient_id = request.query_params.get('patient_id')
        
        if not patient_id:
            return Response(
                {'error': 'patient_id gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient = Patient.objects.get(id=patient_id)
            
            # Toplam tedavi ücreti
            total_treatment_cost = patient.treatments.aggregate(
                total=Sum('price')
            )['total'] or 0
            
            # Toplam ödenen tutar
            total_paid = patient.payments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            # Kalan bakiye
            remaining_balance = total_treatment_cost - total_paid
            
            return Response({
                'patient_id': patient.id,
                'patient_name': patient.get_full_name(),
                'total_treatment_cost': float(total_treatment_cost),
                'total_paid': float(total_paid),
                'remaining_balance': float(remaining_balance)
            })
        
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Hasta bulunamadı'},
                status=status.HTTP_404_NOT_FOUND
            )


class PriceListViewSet(viewsets.ModelViewSet):
    """Price List ViewSet"""
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
