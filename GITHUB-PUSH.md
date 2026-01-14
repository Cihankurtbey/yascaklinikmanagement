# GitHub'a Push Etme Kılavuzu

## 📋 Adım Adım GitHub'a Push

### 1. GitHub'da Repository Oluşturma

1. GitHub.com'a gidin ve giriş yapın
2. Sağ üstteki "+" butonuna tıklayın → "New repository"
3. Repository bilgilerini doldurun:
   - **Repository name:** `yasacklinik` (veya istediğiniz isim)
   - **Description:** "Yaşça Diş Hekimliği Hasta Yönetim Sistemi"
   - **Visibility:** Private (önerilen) veya Public
   - **Initialize:** ❌ README, .gitignore, license eklemeyin (zaten var)
4. "Create repository" butonuna tıklayın

### 2. Git Repository'sini Başlatma

Proje klasöründe şu komutları çalıştırın:

```powershell
# Git repository'sini başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Yaşça Klinik Hasta Yönetim Sistemi"

# GitHub repository'nizi ekleyin (URL'yi kendi repository'nizle değiştirin)
git remote add origin https://github.com/KULLANICI_ADINIZ/yasacklinik.git

# Ana branch'i main olarak ayarlayın
git branch -M main

# GitHub'a push edin
git push -u origin main
```

### 3. Detaylı Komutlar (Adım Adım)

#### Adım 1: Git'i başlat
```powershell
git init
```

#### Adım 2: Dosyaları ekle
```powershell
git add .
```

#### Adım 3: İlk commit
```powershell
git commit -m "Initial commit: Yaşça Klinik Hasta Yönetim Sistemi

- Django REST Framework backend
- React frontend
- MySQL database
- Docker Compose setup
- Modüler mimari
- Responsive tasarım"
```

#### Adım 4: GitHub repository'nizi ekleyin
```powershell
# ÖRNEK (kendi repository URL'nizi kullanın):
git remote add origin https://github.com/KULLANICI_ADINIZ/yasacklinik.git
```

#### Adım 5: Branch adını ayarlayın
```powershell
git branch -M main
```

#### Adım 6: GitHub'a push edin
```powershell
git push -u origin main
```

### 4. GitHub Authentication

Eğer push sırasında authentication hatası alırsanız:

#### Seçenek 1: Personal Access Token (Önerilen)
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "Generate new token (classic)"
3. İsim verin ve süre seçin
4. **repo** scope'unu seçin
5. Token'ı kopyalayın
6. Push sırasında şifre yerine token'ı kullanın

#### Seçenek 2: GitHub CLI
```powershell
# GitHub CLI yükleyin: https://cli.github.com/
gh auth login
```

#### Seçenek 3: SSH Key
```powershell
# SSH key oluştur
ssh-keygen -t ed25519 -C "your_email@example.com"

# Public key'i GitHub'a ekleyin
# Settings → SSH and GPG keys → New SSH key
```

### 5. Sonraki Push'lar

Değişiklik yaptıktan sonra:

```powershell
# Değişiklikleri kontrol et
git status

# Değişiklikleri ekle
git add .

# Commit yap
git commit -m "Açıklayıcı commit mesajı"

# Push et
git push
```

## 🔒 Güvenlik Notları

### ÖNEMLİ: Şunları GitHub'a PUSH ETMEYİN!

- `.env` dosyaları (gizli bilgiler içerir)
- `SECRET_KEY` değerleri
- Veritabanı şifreleri
- API key'leri
- `node_modules/` klasörü (zaten .gitignore'da)
- `__pycache__/` klasörleri

### Güvenli Dosyalar

✅ Push edilebilir:
- `docker-compose.yml` (şifreler environment variable olarak)
- `requirements.txt`
- `package.json`
- Kaynak kodlar
- README.md
- .gitignore

## 📝 Örnek .env Dosyası

GitHub'a push etmeden önce `.env.example` dosyası oluşturun:

```bash
# .env.example (bu dosyayı push edebilirsiniz)
SECRET_KEY=your-secret-key-here
DEBUG=1
MYSQL_DATABASE=yasacklinik_db
MYSQL_USER=yasacklinik_user
MYSQL_PASSWORD=your-password-here
```

## 🚀 Hızlı Başlangıç Scripti

Aşağıdaki komutları sırayla çalıştırın:

```powershell
# 1. Git başlat
git init

# 2. Dosyaları ekle
git add .

# 3. Commit yap
git commit -m "Initial commit: Yaşça Klinik Hasta Yönetim Sistemi"

# 4. Remote ekle (KENDİ URL'NİZİ KULLANIN)
git remote add origin https://github.com/KULLANICI_ADINIZ/yasacklinik.git

# 5. Branch ayarla
git branch -M main

# 6. Push et
git push -u origin main
```

## ❓ Sorun Giderme

### "remote origin already exists" hatası
```powershell
git remote remove origin
git remote add origin https://github.com/KULLANICI_ADINIZ/yasacklinik.git
```

### "Authentication failed" hatası
- Personal Access Token kullanın
- Veya SSH key kurulumu yapın

### "Large files" hatası
```powershell
# Büyük dosyaları kontrol et
git ls-files | ForEach-Object { Get-Item $_ | Select-Object Name, Length }

# .gitignore'a ekleyin
```

## 📚 Ek Kaynaklar

- [GitHub Docs](https://docs.github.com/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
