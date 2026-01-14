# Yaşça Klinik - Kurulum Kılavuzu

## Seçenek 1: Docker ile Kurulum (Önerilen)

### Gereksinimler
- Docker Desktop (Windows için): https://www.docker.com/products/docker-desktop/
- Docker Desktop'ı indirip yükleyin

### Kurulum Adımları

1. **Docker Desktop'ı başlatın** ve çalıştığından emin olun

2. **Proje klasörüne gidin:**
   ```powershell
   cd "C:\Users\CIHAN\OneDrive\Masaüstü\YaşcaKlinik"
   ```

3. **Docker Compose ile başlatın:**
   ```powershell
   docker compose up -d
   ```
   
   Veya eski versiyon için:
   ```powershell
   docker-compose up -d
   ```

4. **Veritabanı migrasyonlarını çalıştırın:**
   ```powershell
   docker compose exec backend python manage.py migrate
   ```

5. **Superuser oluşturun:**
   ```powershell
   docker compose exec backend python manage.py createsuperuser
   ```

6. **Uygulamaya erişin:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

---

## Seçenek 2: Manuel Kurulum (Docker Olmadan)

### Backend Kurulumu

1. **Python 3.11+ yükleyin** (https://www.python.org/downloads/)

2. **MySQL yükleyin ve başlatın** (https://dev.mysql.com/downloads/mysql/)

3. **Virtual environment oluşturun:**
   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Bağımlılıkları yükleyin:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **MySQL için mysqlclient yükleme (Windows):**
   - https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
   - İndirip yükleyin: `pip install mysqlclient‑*.whl`

6. **.env dosyası oluşturun** (backend klasöründe):
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=1
   MYSQL_DATABASE=yasacklinik_db
   MYSQL_USER=root
   MYSQL_PASSWORD=your-mysql-password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   ```

7. **Veritabanını oluşturun:**
   ```sql
   CREATE DATABASE yasacklinik_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

8. **Migrasyonları çalıştırın:**
   ```powershell
   python manage.py migrate
   ```

9. **Superuser oluşturun:**
   ```powershell
   python manage.py createsuperuser
   ```

10. **Backend'i başlatın:**
    ```powershell
    python manage.py runserver
    ```

### Frontend Kurulumu

1. **Node.js 18+ yükleyin** (https://nodejs.org/)

2. **Frontend klasörüne gidin:**
   ```powershell
   cd frontend
   ```

3. **Bağımlılıkları yükleyin:**
   ```powershell
   npm install
   ```

4. **.env dosyası oluşturun** (frontend klasöründe):
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

5. **Frontend'i başlatın:**
   ```powershell
   npm start
   ```

6. **Uygulamaya erişin:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

---

## Sorun Giderme

### Docker sorunları:
- Docker Desktop'ın çalıştığından emin olun
- WSL 2'nin yüklü olduğundan emin olun (Windows için)
- Docker Desktop ayarlarından "Use WSL 2 based engine" seçeneğini etkinleştirin

### MySQL bağlantı sorunları:
- MySQL servisinin çalıştığından emin olun
- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- Port 3306'nın açık olduğundan emin olun

### Port çakışmaları:
- 3000 ve 8000 portlarının kullanılmadığından emin olun
- Gerekirse docker-compose.yml'de portları değiştirin

---

## İlk Kullanım

1. **Admin panelinden kullanıcı oluşturun:**
   - http://localhost:8000/admin adresine gidin
   - Superuser ile giriş yapın
   - Users > Add User ile yeni kullanıcılar ekleyin

2. **Frontend'den giriş yapın:**
   - http://localhost:3000 adresine gidin
   - Oluşturduğunuz kullanıcı ile giriş yapın

3. **Demo modu:**
   - Login sayfasında herhangi bir e-posta ve şifre ile giriş yapabilirsiniz (backend'de demo modu aktifse)
