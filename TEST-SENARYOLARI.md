# Yaşça Klinik - Test Senaryoları

## 🧪 Test Senaryoları

### 1. Giriş ve Kimlik Doğrulama

#### Test 1.1: Başarılı Giriş
1. Tarayıcıda http://localhost:3000 adresine gidin
2. Login sayfasında:
   - E-posta: `admin@yasacklinik.com`
   - Şifre: `admin123`
3. "Giriş Yap" butonuna tıklayın
4. **Beklenen:** Dashboard sayfasına yönlendirilmeli

#### Test 1.2: Hatalı Giriş
1. Yanlış e-posta/şifre ile giriş yapmayı deneyin
2. **Beklenen:** Hata mesajı gösterilmeli

#### Test 1.3: Çıkış
1. Sağ üstteki "Çıkış" butonuna tıklayın
2. **Beklenen:** Login sayfasına yönlendirilmeli

---

### 2. Dashboard (Ana Sayfa)

#### Test 2.1: İstatistikler
1. Dashboard'da şu bilgiler görünmeli:
   - Bugünkü Randevular
   - Bekleyen Hastalar
   - Toplam Hasta
2. **Beklenen:** Sayılar doğru görüntülenmeli

#### Test 2.2: Bugünün Randevuları
1. Dashboard'da "Bugünün Randevuları" listesi görünmeli
2. Her randevu için:
   - Saat
   - Hasta adı
   - İşlem
   - Durum (Tamamlandı, Bekliyor)
3. **Beklenen:** Randevular listelenmeli

---

### 3. Hasta Yönetimi

#### Test 3.1: Hasta Listesi
1. "Hastalar" menüsüne tıklayın
2. **Beklenen:** Hasta listesi görüntülenmeli

#### Test 3.2: Hasta Arama
1. Arama çubuğuna hasta adı, soyadı veya telefon yazın
2. **Beklenen:** İlgili hastalar filtrelenmeli

#### Test 3.3: Yeni Hasta Ekleme
1. "Yeni Hasta Ekle" butonuna tıklayın
2. Formu doldurun:
   - Ad: Test
   - Soyad: Hasta
   - Telefon: 0532 123 4567
   - TC Kimlik No: (opsiyonel)
   - Doğum Tarihi: (opsiyonel)
   - Adres: (opsiyonel)
   - Notlar: (opsiyonel)
3. "Kaydet" butonuna tıklayın
4. **Beklenen:** 
   - Başarı mesajı gösterilmeli
   - Modal kapanmalı
   - Hasta listesine eklenmeli

#### Test 3.4: Hasta Detayı
1. Bir hastanın "Detay" butonuna tıklayın
2. **Beklenen:** Hasta detay sayfası açılmalı

---

### 4. Hasta Detay Sayfası

#### Test 4.1: Profil Bilgileri
1. "Profil Bilgileri" tabında:
   - Kişisel bilgiler görünmeli
   - "Düzenle" butonu çalışmalı
2. Düzenleme yapıp kaydedin
3. **Beklenen:** Bilgiler güncellenmeli

#### Test 4.2: Anamnez
1. "Anamnez" tabına geçin
2. "Anamnezi Düzenle" butonuna tıklayın
3. Formu doldurun:
   - Tıbbi Geçmiş
   - Alerjiler (kırmızı uyarı ile)
   - İlaçlar
   - vb.
4. "Kaydet" butonuna tıklayın
5. **Beklenen:** Anamnez kaydedilmeli ve görüntülenmeli

#### Test 4.3: Tedavi Geçmişi
1. "Tedavi Geçmişi" tabına geçin
2. **Beklenen:** 
   - Tedaviler kronolojik sırada listelenmeli
   - Her tedavi için: Tarih, Doktor, İşlem, Diş numarası görünmeli

#### Test 4.4: Diş Şeması (Odontogram)
1. "Diş Şeması" tabına geçin
2. **Beklenen:**
   - Üst ve alt çene görünmeli
   - Olgun/Süt dişleri geçişi çalışmalı
   - Dişlere tıklanabilmeli
   - Renk kodlu durumlar görünmeli
   - Legend (açıklama) görünmeli

---

### 5. Randevu Yönetimi

#### Test 5.1: Günlük Görünüm
1. "Randevular" menüsüne tıklayın
2. "Günlük" görünümü seçili olmalı
3. **Beklenen:**
   - Saat dilimleri listelenmeli
   - Boş dolu durumları görünmeli
   - Randevular görünmeli

#### Test 5.2: Haftalık Görünüm
1. "Haftalık" butonuna tıklayın
2. **Beklenen:**
   - Haftalık takvim grid görünmeli
   - Her gün için randevular görünmeli

#### Test 5.3: Tarih Navigasyonu
1. "‹" (önceki) butonuna tıklayın
2. "›" (sonraki) butonuna tıklayın
3. "Bugün" butonuna tıklayın
4. **Beklenen:** Tarih değişmeli ve randevular güncellenmeli

#### Test 5.4: Yeni Randevu Ekleme
1. Boş bir saat dilimine tıklayın
2. Modal açılmalı
3. Formu doldurun:
   - Tarih: (otomatik dolu)
   - Saat: (otomatik dolu)
   - Hasta: Bir hasta seçin
   - İşlem: "Kontrol"
   - Notlar: (opsiyonel)
4. "Kaydet" butonuna tıklayın
5. **Beklenen:**
   - Randevu oluşturulmalı
   - Takvimde görünmeli
   - Başarı mesajı gösterilmeli

#### Test 5.5: Randevu Düzenleme
1. Mevcut bir randevuya tıklayın
2. Modal açılmalı (randevu bilgileri dolu)
3. Durumu "Tamamlandı" olarak değiştirin
4. "Kaydet" butonuna tıklayın
5. **Beklenen:** Randevu güncellenmeli

#### Test 5.6: Randevu İptal Etme
1. Bir randevuya tıklayın
2. "İptal Et" butonuna tıklayın
3. Onaylayın
4. **Beklenen:** Randevu iptal edilmeli

---

### 6. Responsive Tasarım Testi

#### Test 6.1: Mobil Görünüm
1. Tarayıcı penceresini küçültün (mobil boyut)
2. **Beklenen:**
   - Tüm sayfalar düzgün görünmeli
   - Menüler erişilebilir olmalı
   - Tablolar kaydırılabilir olmalı

#### Test 6.2: Tablet Görünüm
1. Orta boy ekran simülasyonu yapın
2. **Beklenen:** Layout düzgün görünmeli

---

### 7. Hata Senaryoları

#### Test 7.1: Ağ Hatası
1. Backend'i durdurun: `docker compose stop backend`
2. Bir işlem yapmayı deneyin
3. **Beklenen:** Hata mesajı gösterilmeli
4. Backend'i başlatın: `docker compose start backend`

#### Test 7.2: Geçersiz Veri
1. Hasta eklerken zorunlu alanları boş bırakın
2. **Beklenen:** Form validasyonu çalışmalı

---

## ✅ Test Kontrol Listesi

- [ ] Giriş/Çıkış çalışıyor
- [ ] Dashboard istatistikleri doğru
- [ ] Hasta listesi görüntüleniyor
- [ ] Hasta arama çalışıyor
- [ ] Yeni hasta eklenebiliyor
- [ ] Hasta detay sayfası açılıyor
- [ ] Profil bilgileri düzenlenebiliyor
- [ ] Anamnez kaydedilebiliyor
- [ ] Tedavi geçmişi görüntüleniyor
- [ ] Diş şeması görüntüleniyor
- [ ] Randevu listesi görüntüleniyor
- [ ] Günlük/Haftalık görünüm çalışıyor
- [ ] Yeni randevu eklenebiliyor
- [ ] Randevu düzenlenebiliyor
- [ ] Randevu iptal edilebiliyor
- [ ] Responsive tasarım çalışıyor

---

## 🐛 Bilinen Sorunlar

Şu an için bilinen sorun yok. Test sırasında bulunan sorunları buraya ekleyin.

---

## 📝 Test Notları

Test sırasında not alınacak alanlar:
- Hangi testler başarılı?
- Hangi testler başarısız?
- Hata mesajları neler?
- Öneriler?
