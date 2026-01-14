from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.appointments.models import Appointment


class NotificationStatus(models.TextChoices):
    PENDING = 'pending', 'Bekliyor'
    SENT = 'sent', 'Gönderildi'
    FAILED = 'failed', 'Başarısız'


class Notification(models.Model):
    """Bildirim Modeli (SMS/WhatsApp)"""
    
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Randevu'
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=[('sms', 'SMS'), ('whatsapp', 'WhatsApp')],
        default='whatsapp',
        verbose_name='Bildirim Tipi'
    )
    
    message = models.TextField(verbose_name='Mesaj')
    recipient_phone = models.CharField(max_length=20, verbose_name='Alıcı Telefon')
    
    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        verbose_name='Durum'
    )
    
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Gönderilme Tarihi')
    error_message = models.TextField(blank=True, null=True, verbose_name='Hata Mesajı')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    
    class Meta:
        verbose_name = 'Bildirim'
        verbose_name_plural = 'Bildirimler'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.appointment.patient.get_full_name()} - {self.get_notification_type_display()} - {self.status}"
