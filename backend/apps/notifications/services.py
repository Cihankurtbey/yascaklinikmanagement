import requests
from django.conf import settings
from django.utils import timezone
from .models import Notification, NotificationStatus


class NotificationService:
    """Bildirim Servisi (SMS/WhatsApp)"""
    
    @staticmethod
    def send_sms(phone, message):
        """SMS gönder (F-012)"""
        try:
            # 3. parti SMS servisi entegrasyonu
            # Örnek: Twilio, Nexmo, vb.
            url = settings.SMS_SERVICE_URL
            api_key = settings.SMS_SERVICE_API_KEY
            
            if not url or not api_key:
                # Demo modu - gerçek gönderim yapılmıyor
                return {
                    'success': True,
                    'message': 'Demo modu: SMS gönderimi simüle edildi',
                    'demo': True
                }
            
            payload = {
                'to': phone,
                'message': message,
                'api_key': api_key
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'SMS başarıyla gönderildi',
                    'response': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'SMS gönderilemedi: {response.status_code}',
                    'error': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'SMS gönderim hatası: {str(e)}',
                'error': str(e)
            }
    
    @staticmethod
    def send_whatsapp(phone, message):
        """WhatsApp mesajı gönder (F-012)"""
        try:
            # 3. parti WhatsApp servisi entegrasyonu
            # Örnek: Twilio WhatsApp API, WhatsApp Business API, vb.
            url = settings.SMS_SERVICE_URL  # Aynı servis kullanılabilir
            api_key = settings.SMS_SERVICE_API_KEY
            
            if not url or not api_key:
                # Demo modu
                return {
                    'success': True,
                    'message': 'Demo modu: WhatsApp mesajı simüle edildi',
                    'demo': True
                }
            
            payload = {
                'to': phone,
                'message': message,
                'type': 'whatsapp',
                'api_key': api_key
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'WhatsApp mesajı başarıyla gönderildi',
                    'response': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'WhatsApp mesajı gönderilemedi: {response.status_code}',
                    'error': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'WhatsApp gönderim hatası: {str(e)}',
                'error': str(e)
            }
    
    @staticmethod
    def send_appointment_notification(appointment):
        """Randevu bildirimi gönder"""
        patient = appointment.patient
        message = f"Sayın {patient.get_full_name()}, {appointment.appointment_date.strftime('%d.%m.%Y')} tarihinde saat {appointment.appointment_time.strftime('%H:%M')} için randevunuz oluşturulmuştur. Yaşça Dental Klinik"
        
        notification = Notification.objects.create(
            appointment=appointment,
            notification_type='whatsapp',
            message=message,
            recipient_phone=patient.phone,
            status=NotificationStatus.PENDING
        )
        
        # WhatsApp mesajı gönder
        result = NotificationService.send_whatsapp(patient.phone, message)
        
        if result['success']:
            notification.status = NotificationStatus.SENT
            notification.sent_at = timezone.now()
        else:
            notification.status = NotificationStatus.FAILED
            notification.error_message = result.get('error', result.get('message', ''))
        
        notification.save()
        return notification
