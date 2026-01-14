from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.patients.models import Patient
from apps.treatments.models import Treatment


class Payment(models.Model):
    """Ödeme Modeli (F-014, F-015)"""
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Hasta'
    )
    
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Tedavi'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Tutar'
    )
    
    description = models.TextField(blank=True, null=True, verbose_name='Açıklama')
    
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Ödeme Tarihi')
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_payments',
        verbose_name='Oluşturan'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    
    class Meta:
        verbose_name = 'Ödeme'
        verbose_name_plural = 'Ödemeler'
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['patient', '-payment_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.amount} TL - {self.payment_date.strftime('%d.%m.%Y')}"


class PriceList(models.Model):
    """Fiyat Listesi Modeli (F-020)"""
    
    treatment_type = models.OneToOneField(
        'treatments.TreatmentType',
        on_delete=models.CASCADE,
        related_name='price_list',
        verbose_name='Tedavi Türü'
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Fiyat'
    )
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Fiyat Listesi'
        verbose_name_plural = 'Fiyat Listeleri'
    
    def __str__(self):
        return f"{self.treatment_type.name} - {self.price} TL"
