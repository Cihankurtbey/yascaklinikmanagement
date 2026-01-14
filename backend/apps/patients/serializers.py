from rest_framework import serializers
from .models import Patient, PatientAnamnesis, PatientDocument
from apps.users.serializers import UserSerializer


class PatientDocumentSerializer(serializers.ModelSerializer):
    """Patient Document Serializer"""
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = PatientDocument
        fields = ('id', 'title', 'file', 'file_type', 'uploaded_by_name', 'uploaded_at')
        read_only_fields = ('uploaded_by', 'uploaded_at')


class PatientAnamnesisSerializer(serializers.ModelSerializer):
    """Patient Anamnesis Serializer"""
    
    class Meta:
        model = PatientAnamnesis
        fields = '__all__'
        read_only_fields = ('updated_at',)


class PatientSerializer(serializers.ModelSerializer):
    """Patient Serializer"""
    full_name = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    anamnesis = PatientAnamnesisSerializer(read_only=True)
    documents = PatientDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'phone',
            'tc_identity_number', 'birth_date', 'address', 'notes',
            'created_by_name', 'created_at', 'updated_at', 'last_visit',
            'anamnesis', 'documents'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'last_visit')
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def to_representation(self, instance):
        """TC kimlik numarasını decrypt et"""
        data = super().to_representation(instance)
        if data.get('tc_identity_number'):
            try:
                data['tc_identity_number'] = instance.decrypt_sensitive_data(data['tc_identity_number'])
            except:
                pass  # Decrypt edilemiyorsa olduğu gibi bırak
        return data


class PatientListSerializer(serializers.ModelSerializer):
    """Patient List Serializer (lightweight)"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'full_name', 'phone', 
                  'tc_identity_number', 'last_visit')
        read_only_fields = ('id', 'last_visit')
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def to_representation(self, instance):
        """TC kimlik numarasını decrypt et"""
        data = super().to_representation(instance)
        if data.get('tc_identity_number'):
            try:
                data['tc_identity_number'] = instance.decrypt_sensitive_data(data['tc_identity_number'])
            except:
                pass  # Decrypt edilemiyorsa olduğu gibi bırak
        return data


class PatientCreateSerializer(serializers.ModelSerializer):
    """Patient Create Serializer"""
    
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'phone', 'tc_identity_number',
                  'birth_date', 'address', 'notes')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
