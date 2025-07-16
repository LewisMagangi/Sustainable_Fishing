#!/bin/bash

# Exit on any error
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py makemigrations users content fishing
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@sustainablefishing.com',
        password='admin123',
        full_name='System Administrator',
        role='admin'
    )
    print('Admin user created successfully!')
else:
    print('Admin user already exists.')
"

echo "Build completed successfully!"
