
# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_app_backend.settings')

# application = get_wsgi_application()





import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_app_backend.settings')

application = get_wsgi_application()

# --- Auto-create superuser on startup ---
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

try:
    User = get_user_model()
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Superuser {username} created successfully")
except OperationalError:
    # Database might not be ready yet (first migration)
    pass

