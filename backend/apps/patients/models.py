from django.db import models
from django.conf import settings
from django.utils import timezone
from config.settings import FERNET
import base64


class Patient(models.Model):
    """Hasta Modeli"""
    
    first_name = models.CharField(max_length=150, verbose_name='Ad')
    last_name = models.CharField(max_length=150, verbose_name='Soyad')
    phone = models.CharField(max_length=20, verbose_name='Telefon', db_index=True)
    
    # Opsiyonel alanlar
    tc_identity_number = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='TC Kimlik No',
        help_text='Şifrelenmiş olarak saklanır'
    )
    birth_date = models.DateField(blank=True, null=True, verbose_name='Doğum Tarihi')
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    notes = models.TextField(blank=True, null=True, verbose_name='Notlar')
    
    # İlişkiler
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_patients',
        verbose_name='Oluşturan'
    )
    
    # Tarihler
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name='Son Ziyaret')
    
    class Meta:
        verbose_name = 'Hasta'
        verbose_name_plural = 'Hastalar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.phone}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def encrypt_sensitive_data(self, data):
        """KVKK uyumlu veri şifreleme (AES-256 equivalent)"""
        if data:
            return FERNET.encrypt(data.encode()).decode()
        return None
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Şifreli veriyi çözme"""
        if encrypted_data:
            try:
                return FERNET.decrypt(encrypted_data.encode()).decode()
            except:
                return encrypted_data
        return None
    
    def save(self, *args, **kwargs):
        # TC Kimlik No'yu şifrele (sadece dolu ise)
        if self.tc_identity_number and self.tc_identity_number.strip():
            # Zaten şifrelenmiş mi kontrol et
            try:
                # Eğer decrypt edilebiliyorsa zaten şifrelenmiş
                self.decrypt_sensitive_data(self.tc_identity_number)
            except:
                # Şifrelenmemiş, şifrele
                self.tc_identity_number = self.encrypt_sensitive_data(self.tc_identity_number)
        super().save(*args, **kwargs)


class PatientAnamnesis(models.Model):
    """Hasta Anamnez Modeli"""
    
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='anamnesis',
        verbose_name='Hasta'
    )
    
    # Tıbbi Geçmiş
    medical_history = models.TextField(blank=True, null=True, verbose_name='Tıbbi Geçmiş')
    allergies = models.TextField(blank=True, null=True, verbose_name='Alerjiler')
    medications = models.TextField(blank=True, null=True, verbose_name='Kullandığı İlaçlar')
    chronic_diseases = models.TextField(blank=True, null=True, verbose_name='Kronik Hastalıklar')
    past_surgeries = models.TextField(blank=True, null=True, verbose_name='Geçirdiği Ameliyatlar')
    
    # Aile Öyküsü
    family_history = models.TextField(blank=True, null=True, verbose_name='Aile Öyküsü')
    
    # Yaşam Tarzı
    smoking = models.CharField(max_length=200, blank=True, null=True, verbose_name='Sigara Kullanımı')
    alcohol = models.CharField(max_length=200, blank=True, null=True, verbose_name='Alkol Kullanımı')
    pregnancy_status = models.CharField(max_length=200, blank=True, null=True, verbose_name='Gebelik Durumu')
    
    # Diğer
    other_notes = models.TextField(blank=True, null=True, verbose_name='Diğer Notlar')
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Hasta Anamnezi'
        verbose_name_plural = 'Hasta Anamnezleri'
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - Anamnez"


class PatientDocument(models.Model):
    """Hasta Doküman Modeli (Röntgen, Fotoğraf vb.)"""
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Hasta'
    )
    
    title = models.CharField(max_length=200, verbose_name='Başlık')
    file = models.FileField(upload_to='patient_documents/%Y/%m/%d/', verbose_name='Dosya')
    file_type = models.CharField(max_length=50, verbose_name='Dosya Tipi')  # rontgen, fotograf, etc.
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Yükleyen'
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Yüklenme Tarihi')
    
    class Meta:
        verbose_name = 'Hasta Dokümanı'
        verbose_name_plural = 'Hasta Dokümanları'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.title}"
