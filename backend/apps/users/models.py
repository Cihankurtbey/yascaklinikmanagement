from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Kullanıcı e-posta adresi gereklidir')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Yönetici'
        DOCTOR = 'doctor', 'Diş Hekimi'
        ASSISTANT = 'assistant', 'Asistan'
    
    email = models.EmailField(unique=True, verbose_name='E-posta')
    first_name = models.CharField(max_length=150, verbose_name='Ad')
    last_name = models.CharField(max_length=150, verbose_name='Soyad')
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ASSISTANT,
        verbose_name='Rol'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_staff = models.BooleanField(default=False, verbose_name='Personel')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Kayıt Tarihi')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Son Giriş')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    
    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR
    
    @property
    def is_assistant(self):
        return self.role == self.Role.ASSISTANT
