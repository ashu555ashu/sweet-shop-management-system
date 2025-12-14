from django.contrib.auth import get_user_model
import django
import os

# Setup Django environment for standalone script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sweetshop.settings')
django.setup()

User = get_user_model()

# Fetch superuser
superuser = User.objects.get(username='ashish_super')

# Update details
superuser.username = 'ashu'
superuser.phone = '8200437457'
superuser.email = 'gohelashish861@gmail.com'
superuser.address = 'New Address, City'
superuser.set_password('ashishgohel')  # always use set_password

# Save changes
superuser.save()

print("Superuser updated successfully!")
