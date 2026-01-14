from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.patients.models import Patient
from apps.users.models import User


class AppointmentStatus(models.TextChoices):
    PENDING = 'pending', 'Bekliyor'
    COMPLETED = 'completed', 'Tamamlandı'
    CANCELLED = 'cancelled', 'İptal'
    NO_SHOW = 'no_show', 'Gelmedi'


class Appointment(models.Model):
    """Randevu Modeli"""
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Hasta'
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        limit_choices_to={'role': User.Role.DOCTOR},
        verbose_name='Doktor'
    )
    
    appointment_date = models.DateField(verbose_name='Randevu Tarihi', db_index=True)
    appointment_time = models.TimeField(verbose_name='Randevu Saati')
    
    procedure = models.CharField(max_length=200, blank=True, null=True, verbose_name='İşlem')
    notes = models.TextField(blank=True, null=True, verbose_name='Notlar')
    
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
        verbose_name='Durum'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_appointments',
        verbose_name='Oluşturan'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'
        ordering = ['appointment_date', 'appointment_time']
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['status']),
        ]
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.appointment_date} {self.appointment_time}"
    
    def clean(self):
        """Randevu çakışmasını kontrol et (F-008)"""
        if self.pk is None:  # Yeni randevu
            conflicting = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time,
                status__in=[AppointmentStatus.PENDING, AppointmentStatus.COMPLETED]
            )
            if conflicting.exists():
                raise ValidationError(
                    'Bu saatte doktora zaten bir randevu kayıtlı. Lütfen farklı bir saat seçin.'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Randevu oluşturulduğunda hasta son ziyaret tarihini güncelle
        if self.status == AppointmentStatus.COMPLETED:
            self.patient.last_visit = timezone.now()
            self.patient.save()


class AppointmentSettings(models.Model):
    """Randevu Ayarları (F-022)"""
    
    start_time = models.TimeField(default='09:00', verbose_name='Başlangıç Saati')
    end_time = models.TimeField(default='18:00', verbose_name='Bitiş Saati')
    slot_duration = models.IntegerField(default=15, verbose_name='Randevu Aralığı (dakika)')
    
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Güncelleyen'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Randevu Ayarı'
        verbose_name_plural = 'Randevu Ayarları'
    
    def __str__(self):
        return f"Randevu Ayarları: {self.start_time} - {self.end_time} ({self.slot_duration} dk)"
    
    def save(self, *args, **kwargs):
        # Tek bir ayar kaydı olmasını sağla
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Randevu ayarlarını getir, yoksa varsayılan oluştur"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
