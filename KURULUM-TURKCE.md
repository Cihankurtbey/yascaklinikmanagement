# Yaşça Klinik - Kurulum Kılavuzu (Türkçe)

## 🐳 Seçenek 1: Docker ile Kurulum (Önerilen)

### Gereksinimler
- **Docker Desktop** (Windows için): [İndir](https://www.docker.com/products/docker-desktop/)
- Docker Desktop'ı indirip yükleyin ve başlatın

### Adım Adım Kurulum

1. **Docker Desktop'ı başlatın**
   - Sistem tepsisinde Docker ikonunun yeşil olduğundan emin olun

2. **PowerShell'i yönetici olarak açın** ve proje klasörüne gidin:
   ```powershell
   cd "C:\Users\CIHAN\OneDrive\Masaüstü\YaşcaKlinik"
   ```

3. **Docker Compose ile tüm servisleri başlatın:**
   ```powershell
   docker compose up -d
   ```
   
   **Not:** Eğer "docker compose" çalışmazsa, eski versiyon için şunu deneyin:
   ```powershell
   docker-compose up -d
   ```

4. **Veritabanı tablolarını oluşturun:**
   ```powershell
   docker compose exec backend python manage.py migrate
   ```

5. **Yönetici kullanıcısı oluşturun:**
   ```powershell
   docker compose exec backend python manage.py createsuperuser
   ```
   - E-posta, ad, soyad ve şifre girin

6. **Uygulamaları açın:**
   - 🌐 **Frontend:** http://localhost:3000
   - 🔧 **Backend API:** http://localhost:8000
   - ⚙️ **Admin Panel:** http://localhost:8000/admin

---

## 💻 Seçenek 2: Manuel Kurulum (Docker Olmadan)

Eğer Docker kullanmak istemiyorsanız, her şeyi manuel olarak kurabilirsiniz.

### Backend Kurulumu (Django)

1. **Python 3.11 veya üstünü yükleyin**
   - [Python İndir](https://www.python.org/downloads/)
   - Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin

2. **MySQL yükleyin ve başlatın**
   - [MySQL İndir](https://dev.mysql.com/downloads/mysql/)
   - MySQL Workbench veya komut satırından veritabanı oluşturun

3. **Backend klasörüne gidin:**
   ```powershell
   cd backend
   ```

4. **Virtual environment oluşturun:**
   ```powershell
   python -m venv venv
   ```

5. **Virtual environment'ı aktifleştirin:**
   ```powershell
   venv\Scripts\activate
   ```

6. **Bağımlılıkları yükleyin:**
   ```powershell
   pip install -r requirements.txt
   ```

7. **MySQL Client için özel kurulum (Windows):**
   - [MySQL Client Wheel Dosyası](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
   - İndirip yükleyin: `pip install mysqlclient‑*.whl`

8. **Backend klasöründe `.env` dosyası oluşturun:**
   ```
   SECRET_KEY=django-insecure-change-this-in-production
   DEBUG=1
   MYSQL_DATABASE=yasacklinik_db
   MYSQL_USER=root
   MYSQL_PASSWORD=your-mysql-password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   ```

9. **MySQL'de veritabanını oluşturun:**
   ```sql
   CREATE DATABASE yasacklinik_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

10. **Django migrasyonlarını çalıştırın:**
    ```powershell
    python manage.py migrate
    ```

11. **Yönetici kullanıcısı oluşturun:**
    ```powershell
    python manage.py createsuperuser
    ```

12. **Backend sunucusunu başlatın:**
    ```powershell
    python manage.py runserver
    ```
    - Backend: http://localhost:8000

### Frontend Kurulumu (React)

1. **Node.js 18 veya üstünü yükleyin**
   - [Node.js İndir](https://nodejs.org/)

2. **Frontend klasörüne gidin:**
   ```powershell
   cd frontend
   ```

3. **Bağımlılıkları yükleyin:**
   ```powershell
   npm install
   ```

4. **Frontend klasöründe `.env` dosyası oluşturun:**
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

5. **Frontend sunucusunu başlatın:**
   ```powershell
   npm start
   ```
   - Frontend: http://localhost:3000

---

## 🔧 Sorun Giderme

### Docker Sorunları

**Problem:** "docker compose" komutu çalışmıyor
- **Çözüm:** `docker-compose` (tire ile) deneyin veya Docker Desktop'ı güncelleyin

**Problem:** Docker Desktop başlamıyor
- **Çözüm:** 
  - WSL 2'nin yüklü olduğundan emin olun
  - Docker Desktop ayarlarından "Use WSL 2 based engine" seçeneğini etkinleştirin
  - Bilgisayarı yeniden başlatın

**Problem:** Port zaten kullanılıyor
- **Çözüm:** 
  - 3000 ve 8000 portlarını kullanan uygulamaları kapatın
  - Veya `docker-compose.yml` dosyasında portları değiştirin

### MySQL Sorunları

**Problem:** MySQL bağlantı hatası
- **Çözüm:**
  - MySQL servisinin çalıştığından emin olun (Windows Services)
  - Kullanıcı adı ve şifrenin doğru olduğundan emin olun
  - Port 3306'nın açık olduğundan emin olun

**Problem:** mysqlclient yüklenemiyor
- **Çözüm:**
  - Visual C++ Build Tools yükleyin
  - Veya önceden derlenmiş wheel dosyasını kullanın

### Frontend Sorunları

**Problem:** npm install hataları
- **Çözüm:**
  - Node.js versiyonunu kontrol edin (18+)
  - `npm cache clean --force` çalıştırın
  - `node_modules` klasörünü silip tekrar `npm install` yapın

---

## 🚀 İlk Kullanım

1. **Admin panelinden kullanıcı oluşturun:**
   - http://localhost:8000/admin adresine gidin
   - Superuser ile giriş yapın
   - Users > Add User ile yeni kullanıcılar ekleyin (Doctor, Assistant, Admin)

2. **Frontend'den giriş yapın:**
   - http://localhost:3000 adresine gidin
   - Oluşturduğunuz kullanıcı ile giriş yapın

3. **Test verileri ekleyin:**
   - Admin panelinden hastalar, randevular ekleyebilirsiniz
   - Veya frontend üzerinden yeni hasta kaydı oluşturabilirsiniz

---

## 📝 Notlar

- **Güvenlik:** Production ortamında mutlaka `SECRET_KEY` ve `ENCRYPTION_KEY` değerlerini değiştirin
- **Veritabanı Yedekleme:** Düzenli olarak veritabanı yedeği alın
- **Loglar:** Docker kullanıyorsanız logları görmek için: `docker compose logs -f`

---

## 🆘 Yardım

Sorun yaşıyorsanız:
1. Hata mesajlarını kontrol edin
2. Log dosyalarını inceleyin
3. Docker/MySQL servislerinin çalıştığından emin olun
