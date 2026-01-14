# 🚀 Hızlı Test Kılavuzu

## ⚡ Hızlı Test Adımları

### 1. Uygulamaya Giriş
- **URL:** http://localhost:3000
- **Kullanıcı:** `admin@yasacklinik.com`
- **Şifre:** `admin123`

### 2. Hasta Ekleme Testi (2 dakika)
1. "Hastalar" menüsüne tıklayın
2. "Yeni Hasta Ekle" butonuna tıklayın
3. Formu doldurun:
   - Ad: **Zeynep**
   - Soyad: **Aydın**
   - Telefon: **0537 111 2233**
   - TC Kimlik No: (boş bırakabilirsiniz)
4. "Kaydet" butonuna tıklayın
5. ✅ **Beklenen:** Hasta listesinde görünmeli

### 3. Randevu Görüntüleme Testi (1 dakika)
1. "Randevular" menüsüne tıklayın
2. Bugünün tarihini kontrol edin
3. ✅ **Beklenen:** 4 randevu görünmeli:
   - 09:00 - Ahmet Yılmaz
   - 10:00 - Ayşe Demir
   - 11:30 - Mehmet Kaya
   - 14:00 - Fatma Şahin

### 4. Randevu Ekleme Testi (2 dakika)
1. Randevular sayfasında boş bir saat dilimine tıklayın (örn: 15:00)
2. Modal açılmalı
3. Hasta seçin (yeni eklediğiniz Zeynep Aydın)
4. İşlem: "Kontrol" yazın
5. "Kaydet" butonuna tıklayın
6. ✅ **Beklenen:** Randevu oluşturulmalı ve 15:00'te görünmeli

### 5. Hasta Detay Testi (2 dakika)
1. "Hastalar" sayfasına gidin
2. Bir hastanın "Detay" butonuna tıklayın
3. Tüm tabları kontrol edin:
   - ✅ Profil Bilgileri
   - ✅ Anamnez (düzenleme yapabilirsiniz)
   - ✅ Tedavi Geçmişi
   - ✅ Diş Şeması

## 🐛 Sorun Görürseniz

### Randevular Görünmüyor
- Browser Console'u açın (F12)
- "Console" tab'ında hata var mı kontrol edin
- "Network" tab'ında `/api/appointments/calendar/` isteği başarılı mı?

### Hasta Eklenmiyor
- Browser Console'u açın (F12)
- "Network" tab'ında `/api/patients/` POST isteği var mı?
- Hata mesajı ne diyor?

### Backend Hatası
```bash
docker compose logs backend --tail 20
```

### Frontend Hatası
```bash
docker compose logs frontend --tail 20
```

## ✅ Başarı Kriterleri

- [x] Hasta eklenebiliyor
- [x] Randevular görüntüleniyor
- [x] Yeni randevu eklenebiliyor
- [x] Hasta detay sayfası açılıyor
- [x] Tüm tablar çalışıyor

## 📞 Yardım

Sorun devam ederse:
1. Browser Console'daki hata mesajlarını paylaşın
2. Network tab'ındaki failed request'leri kontrol edin
3. Backend loglarını kontrol edin
