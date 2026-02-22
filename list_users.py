import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User

for user in User.objects.all():
    print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")
