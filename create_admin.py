import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
email = 'admin@example.com'
password = 'adminpassword123'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        first_name='Admin',
        last_name='User'
    )
    print(f"Superuser created: {email}")
else:
    user = User.objects.get(email=email)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"Superuser updated: {email}")
