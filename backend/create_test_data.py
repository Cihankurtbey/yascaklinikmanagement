#!/usr/bin/env python
"""Script to create test data"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.patients.models import Patient
from apps.appointments.models import Appointment, AppointmentStatus
from apps.treatments.models import TreatmentType, Treatment, TreatmentStatus

# Kullanıcılar oluştur
if not User.objects.filter(role=User.Role.DOCTOR).exists():
    doctor = User.objects.create_user(
        email='doctor@yasacklinik.com',
        password='doctor123',
        first_name='Ayşe',
        last_name='Kaya',
        role=User.Role.DOCTOR
    )
    print(f'Doktor oluşturuldu: {doctor.email}')
else:
    doctor = User.objects.filter(role=User.Role.DOCTOR).first()

if not User.objects.filter(role=User.Role.ASSISTANT).exists():
    assistant = User.objects.create_user(
        email='asistan@yasacklinik.com',
        password='asistan123',
        first_name='Mehmet',
        last_name='Demir',
        role=User.Role.ASSISTANT
    )
    print(f'Asistan oluşturuldu: {assistant.email}')
else:
    assistant = User.objects.filter(role=User.Role.ASSISTANT).first()

# Hastalar oluştur
patients_data = [
    {
        'first_name': 'Ahmet',
        'last_name': 'Yılmaz',
        'phone': '0532 123 4567',
        'birth_date': '1985-05-15',
        'address': 'Atatürk Mah. Cumhuriyet Cad. No:45 Daire:3 Ankara',
        'notes': 'Penisilin alerjisi var',
    },
    {
        'first_name': 'Ayşe',
        'last_name': 'Demir',
        'phone': '0533 234 5678',
        'birth_date': '1990-08-20',
    },
    {
        'first_name': 'Mehmet',
        'last_name': 'Kaya',
        'phone': '0534 345 6789',
    },
    {
        'first_name': 'Fatma',
        'last_name': 'Şahin',
        'phone': '0535 456 7890',
    },
    {
        'first_name': 'Ali',
        'last_name': 'Öz',
        'phone': '0536 567 8901',
    },
]

created_patients = []
for patient_data in patients_data:
    patient, created = Patient.objects.get_or_create(
        phone=patient_data['phone'],
        defaults={**patient_data, 'created_by': assistant}
    )
    if created:
        # TC kimlik numarasını şifrelemeden ekle (test için)
        if 'tc_identity_number' in patient_data:
            patient.tc_identity_number = patient_data['tc_identity_number']
            patient.save(update_fields=['tc_identity_number'])
        created_patients.append(patient)
        print(f'Hasta oluşturuldu: {patient.get_full_name()}')

# Tedavi türleri oluştur
treatment_types_data = [
    {'name': 'Dolgu', 'default_price': 500.00, 'color_code': '#3b82f6'},
    {'name': 'Kanal Tedavisi', 'default_price': 1500.00, 'color_code': '#ef4444'},
    {'name': 'Kron', 'default_price': 2000.00, 'color_code': '#fbbf24'},
    {'name': 'Çekildi', 'default_price': 300.00, 'color_code': '#6b7280'},
    {'name': 'İmplant', 'default_price': 5000.00, 'color_code': '#a855f7'},
    {'name': 'Detartraj', 'default_price': 400.00, 'color_code': '#10b981'},
]

for tt_data in treatment_types_data:
    tt, created = TreatmentType.objects.get_or_create(
        name=tt_data['name'],
        defaults=tt_data
    )
    if created:
        print(f'Tedavi türü oluşturuldu: {tt.name}')

# Randevular oluştur
if created_patients:
    today = datetime.now().date()
    times = ['09:00', '10:00', '11:30', '14:00', '15:00']
    
    for i, patient in enumerate(created_patients[:4]):
        if i < len(times):
            appointment, created = Appointment.objects.get_or_create(
                patient=patient,
                doctor=doctor,
                appointment_date=today,
                appointment_time=times[i],
                defaults={
                    'procedure': ['Kontrol', 'Dolgu', 'Kanal Tedavisi', 'Diş Temizliği'][i],
                    'status': AppointmentStatus.PENDING if i > 0 else AppointmentStatus.COMPLETED,
                    'created_by': assistant,
                }
            )
            if created:
                print(f'Randevu oluşturuldu: {patient.get_full_name()} - {times[i]}')

print('\n✅ Test verileri oluşturuldu!')
print(f'\nGiriş bilgileri:')
print(f'Admin: admin@yasacklinik.com / admin123')
print(f'Doktor: doctor@yasacklinik.com / doctor123')
print(f'Asistan: asistan@yasacklinik.com / asistan123')
