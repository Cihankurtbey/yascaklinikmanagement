# Yaşça Diş Hekimliği Hasta Yönetim Sistemi

Modern, modüler ve responsive bir diş klinik yönetim sistemi.

## 🏗️ Mimari

- **Frontend**: React (TypeScript)
- **Backend**: Django REST Framework (Python)
- **Veritabanı**: MySQL
- **Containerization**: Docker & Docker Compose

## 📁 Proje Yapısı

```
YaşcaKlinik/
├── backend/          # Django backend
│   ├── apps/         # Modüler Django uygulamaları
│   ├── config/       # Django ayarları
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/   # Yeniden kullanılabilir componentler
│   │   ├── features/     # Feature-based modüller
│   │   ├── services/     # API servisleri
│   │   └── utils/        # Yardımcı fonksiyonlar
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🚀 Kurulum

```bash
docker-compose up -d
```

## 👥 Kullanıcı Rolleri

- **Diş Hekimi (Doctor)**: Tedavi girişleri, diş şeması, randevu takvimi
- **Asistan/Sekreter (Assistant)**: Hasta kaydı, randevu oluşturma
- **Yönetici (Admin)**: Kullanıcı yönetimi, sistem ayarları

## 📋 Özellikler

- ✅ Kullanıcı Yönetimi ve RBAC
- ✅ Hasta Yönetimi
- ✅ Randevu Yönetimi (Günlük/Haftalık/Aylık)
- ✅ Tedavi Yönetimi ve Odontogram
- ✅ Bildirim Sistemi (SMS/WhatsApp)
- ✅ Finansal Yönetim
- ✅ Doküman Yönetimi
- ✅ Raporlama ve Dashboard

## 🔒 Güvenlik

- HTTPS/SSL şifreleme
- AES-256 veri şifreleme
- Session timeout (30 dakika)
- KVKK uyumlu veri saklama

## 📝 Lisans

Bu proje bitirme projesi olarak geliştirilmiştir.
