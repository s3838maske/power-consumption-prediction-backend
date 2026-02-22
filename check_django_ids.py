import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User

print("Checking User IDs through Django...")
for user in User.objects.all():
    print(f"Email: {user.email}, ID: {user.id}, Is Staff: {user.is_staff}")
