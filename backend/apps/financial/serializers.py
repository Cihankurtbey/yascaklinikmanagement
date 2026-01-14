from rest_framework import serializers
from .models import Payment, PriceList
from apps.patients.serializers import PatientListSerializer
from apps.treatments.serializers import TreatmentListSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """Payment Serializer"""
    patient_detail = PatientListSerializer(source='patient', read_only=True)
    treatment_detail = TreatmentListSerializer(source='treatment', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = (
            'id', 'patient', 'patient_detail', 'treatment', 'treatment_detail',
            'amount', 'description', 'payment_date', 'created_by_name', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Payment Create Serializer"""
    
    class Meta:
        model = Payment
        fields = ('patient', 'treatment', 'amount', 'description', 'payment_date')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PriceListSerializer(serializers.ModelSerializer):
    """Price List Serializer"""
    treatment_type_name = serializers.CharField(source='treatment_type.name', read_only=True)
    
    class Meta:
        model = PriceList
        fields = ('id', 'treatment_type', 'treatment_type_name', 'price', 'updated_at')
        read_only_fields = ('id', 'updated_at')
