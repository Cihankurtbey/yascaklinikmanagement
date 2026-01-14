from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.patients.models import Patient
from apps.users.models import User


class TreatmentType(models.Model):
    """Tedavi Türü Modeli (F-020)"""
    
    name = models.CharField(max_length=200, unique=True, verbose_name='Tedavi Adı')
    default_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Varsayılan Fiyat'
    )
    color_code = models.CharField(max_length=7, default='#000000', verbose_name='Renk Kodu')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Tedavi Türü'
        verbose_name_plural = 'Tedavi Türleri'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TreatmentStatus(models.TextChoices):
    PLANNED = 'planned', 'Yapılacak'
    COMPLETED = 'completed', 'Tamamlanmış'


class Odontogram(models.Model):
    """Odontogram Modeli - Diş Şeması"""
    
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='odontogram',
        verbose_name='Hasta'
    )
    
    # Olgun dişler için JSON field (FDI notasyonu: 11-18, 21-28, 31-38, 41-48)
    permanent_teeth = models.JSONField(default=dict, verbose_name='Olgun Dişler')
    
    # Süt dişleri için JSON field (FDI notasyonu: 51-55, 61-65, 71-75, 81-85)
    primary_teeth = models.JSONField(default=dict, verbose_name='Süt Dişleri')
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Odontogram'
        verbose_name_plural = 'Odontogramlar'
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - Odontogram"


class Treatment(models.Model):
    """Tedavi Modeli"""
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='treatments',
        verbose_name='Hasta'
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='treatments',
        limit_choices_to={'role': User.Role.DOCTOR},
        verbose_name='Doktor'
    )
    
    treatment_type = models.ForeignKey(
        TreatmentType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='treatments',
        verbose_name='Tedavi Türü'
    )
    
    tooth_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Diş Numarası',
        help_text='FDI notasyonu (örn: 16, 21, 36)'
    )
    
    is_primary_tooth = models.BooleanField(default=False, verbose_name='Süt Dişi')
    
    description = models.TextField(verbose_name='Açıklama')
    
    status = models.CharField(
        max_length=20,
        choices=TreatmentStatus.choices,
        default=TreatmentStatus.PLANNED,
        verbose_name='Durum'
    )
    
    treatment_date = models.DateTimeField(default=timezone.now, verbose_name='Tedavi Tarihi')
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Fiyat'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Tedavi'
        verbose_name_plural = 'Tedaviler'
        ordering = ['-treatment_date']
        indexes = [
            models.Index(fields=['patient', '-treatment_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.treatment_type.name if self.treatment_type else 'Tedavi'} - {self.treatment_date.strftime('%d.%m.%Y')}"
    
    def save(self, *args, **kwargs):
        # Fiyat belirtilmemişse varsayılan fiyatı kullan
        if not self.price and self.treatment_type:
            self.price = self.treatment_type.default_price
        
        super().save(*args, **kwargs)
        
        # Odontogram'ı güncelle
        self.update_odontogram()
    
    def update_odontogram(self):
        """Tedavi kaydedildiğinde odontogram'ı güncelle"""
        odontogram, created = Odontogram.objects.get_or_create(patient=self.patient)
        
        teeth_data = odontogram.primary_teeth if self.is_primary_tooth else odontogram.permanent_teeth
        
        if self.tooth_number:
            if self.tooth_number not in teeth_data:
                teeth_data[self.tooth_number] = []
            
            treatment_data = {
                'treatment_id': self.id,
                'treatment_type': self.treatment_type.name if self.treatment_type else '',
                'status': self.status,
                'date': self.treatment_date.isoformat(),
            }
            
            # Aynı tedavi varsa güncelle, yoksa ekle
            existing = None
            for idx, item in enumerate(teeth_data[self.tooth_number]):
                if item.get('treatment_id') == self.id:
                    existing = idx
                    break
            
            if existing is not None:
                teeth_data[self.tooth_number][existing] = treatment_data
            else:
                teeth_data[self.tooth_number].append(treatment_data)
            
            if self.is_primary_tooth:
                odontogram.primary_teeth = teeth_data
            else:
                odontogram.permanent_teeth = teeth_data
            
            odontogram.save()
