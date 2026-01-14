from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Patient, PatientAnamnesis, PatientDocument
from .serializers import (
    PatientSerializer,
    PatientListSerializer,
    PatientCreateSerializer,
    PatientAnamnesisSerializer,
    PatientDocumentSerializer
)
from apps.users.permissions import IsAssistantOrAbove


class PatientViewSet(viewsets.ModelViewSet):
    """Patient ViewSet"""
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated, IsAssistantOrAbove]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone']
    ordering_fields = ['created_at', 'last_visit', 'first_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PatientCreateSerializer
        elif self.action == 'list':
            return PatientListSerializer
        return PatientSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Arama parametresi
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )
        return queryset
    
    @action(detail=True, methods=['get', 'put', 'patch'])
    def anamnesis(self, request, pk=None):
        """Get or update patient anamnesis"""
        patient = self.get_object()
        anamnesis, created = PatientAnamnesis.objects.get_or_create(patient=patient)
        
        if request.method == 'GET':
            serializer = PatientAnamnesisSerializer(anamnesis)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = PatientAnamnesisSerializer(
                anamnesis,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'post'])
    def documents(self, request, pk=None):
        """Get or add patient documents"""
        patient = self.get_object()
        
        if request.method == 'GET':
            documents = patient.documents.all()
            serializer = PatientDocumentSerializer(documents, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = PatientDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(patient=patient, uploaded_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
