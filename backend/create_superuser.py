#!/usr/bin/env python
"""Script to create superuser non-interactively"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

# Superuser oluştur
if not User.objects.filter(email='admin@yasacklinik.com').exists():
    User.objects.create_superuser(
        email='admin@yasacklinik.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role=User.Role.ADMIN
    )
    print('Superuser oluşturuldu: admin@yasacklinik.com / admin123')
else:
    print('Superuser zaten mevcut!')
