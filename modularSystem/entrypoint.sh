#!/bin/sh

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
python manage.py migrate

# Create superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Start server
exec "$@"