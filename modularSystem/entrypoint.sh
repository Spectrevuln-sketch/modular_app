#!/bin/sh

# Tunggu hingga database siap
echo "Waiting for database..."
max_retries=10
retry_delay=5

for i in $(seq 1 $max_retries); do
    if python -c "import socket; \
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); \
        s.settimeout(1); \
        s.connect(('$DB_HOST', $DB_PORT)); \
        s.close()" 2>/dev/null; then
        echo "Database is ready!"
        break
    else
        echo "Attempt $i/$max_retries: Database not ready. Retrying in $retry_delay seconds..."
        sleep $retry_delay
    fi
done

# Jalankan migrasi
python manage.py migrate --noinput

# Inisialisasi aplikasi
python manage.py init_app  # Buat command kustom jika diperlukan

# Kumpulkan static files jika belum dilakukan
python manage.py collectstatic --noinput

# Jalankan server
exec "$@"