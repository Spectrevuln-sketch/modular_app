# Modular Django System

Sistem modular Django untuk manajemen aplikasi dinamis dengan fitur instalasi, upgrade, dan uninstall modul secara real-time.

---

## 🔑 Fitur Utama

- 🧩 **Manajemen Modul Dinamis**: Instal, upgrade, dan uninstall modul tanpa restart server
- 🔒 **Sistem Permission Berbasis Role**: 3 level akses (Manager, User, Public)
- 🚀 **Landing Page Otomatis**: Halaman produk otomatis dibuat saat modul diinstal
- 📊 **Dashboard Monitoring**: Pantau status sistem dan modul
- ♻️ **Auto Migration Handling**: Migrasi database otomatis saat upgrade modul

---

## 🗂️ Struktur Direktori

```yaml
-- README.md
-- db.sqlite3
-- engine_module/
   -- migrations/
   -- templates/
   -- templatetags/
   -- __init__.py
   -- admin.py
   -- apps.py
   -- middleware.py
   -- models.py
   -- module_loader.py
   -- urls.py
   `-- views.py
-- manage.py
-- modularSystem/
   -- settings.py
   -- urls.py
   `-- wsgi.py
-- modules/
   -- module_discovery.py
   `-- product_module/
       -- migrations/
       -- templates/
       -- __init__.py
       -- admin.py
       -- apps.py
       -- forms.py
       -- models.py
       -- permission.py
       -- urls.py
       `-- views.py
-- requirements.txt
`-- templates/
    `-- admin/
        `-- base_site.html
```

---

## 🧰 Prasyarat

- Python 3.9+
- PostgreSQL (disarankan) atau SQLite
- Virtualenv (direkomendasikan)

---

## 🚀 Instalasi

### 1. Clone Repositori

```bash
git clone https://github.com/username/modular-django-system.git
cd modular-django-system
```

### 2. Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Instal Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Database

Edit di `modularSystem/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'modular_db',
        'USER': 'modular_user',
        'PASSWORD': 'passwordkuat123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Migrasi Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Buat Superuser

```bash
python manage.py createsuperuser
```

### 7. Jalankan Server

```bash
python manage.py runserver
```

Akses: [http://localhost:8000](http://localhost:8000)

---

## 🧭 Penggunaan

### 1. Manajemen Modul

Akses: [http://localhost:8000/modules/](http://localhost:8000/modules/)

- **Install**: Aktifkan modul baru
- **Upgrade**: Perbarui modul ke versi terbaru
- **Uninstall**: Nonaktifkan modul

### 2. Modul Produk

Setelah menginstal modul produk: [http://localhost:8000/products/](http://localhost:8000/products/)

- ✅ Tambah produk
- 🔍 Lihat daftar produk
- ✏️ Edit produk
- 🗑️ Hapus produk

### 3. Sistem Permission

3 level akses:

- **Manager** (CRUD)
- **User** (CRU)
- **Public** (R)

Atur melalui: [http://localhost:8000/admin/auth/group/](http://localhost:8000/admin/auth/group/)

### 4. Health Check

Akses: [http://localhost:8000/](http://localhost:8000/)

Contoh respons:

```json
{
  "status": "ok",
  "message": "Health check successful",
  "services": {
    "database": "connected",
    "cache": "active"
  }
}
```

---

## ➕ Menambahkan Modul Baru

1. Buat aplikasi baru:

```bash
python manage.py startapp {nama module}_module modules/{nama module}_module
```

2. Daftar modul di `apps.py`:

```python
from django.apps import AppConfig

class NewModuleConfig(AppConfig):
    name = 'modules.{nama module}_module'
    verbose_name = 'New Module'

    def ready(self):
        from . import signals
```

3. Tambahkan ke `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'modules.{nama module}_module.apps.NewModuleConfig',
]
```

4. Buat migrasi:

```bash
python manage.py makemigrations {nama module}_module
python manage.py migrate {nama module}_module
```

Modul akan otomatis muncul di halaman manajemen modul.

## 🔨 System Design

[Flow Chart](https://www.mermaidchart.com/app/projects/a02d5590-2a76-4b7a-9b65-aff6c91aaf13/diagrams/fc4c6e1e-fa19-4a54-b407-bd845cfdc78e/version/v0.1/edit)
 | [ERD](https://www.mermaidchart.com/app/projects/a02d5590-2a76-4b7a-9b65-aff6c91aaf13/diagrams/ac088f0e-8bb5-4a80-a352-d3c13ae05b13/version/v0.1/edit)
 | [Architecture](https://www.mermaidchart.com/app/projects/a02d5590-2a76-4b7a-9b65-aff6c91aaf13/diagrams/03d46f82-3d03-44ba-a97c-1e5d0265a46c/version/v0.1/edit)

---

## 🧪 Lingkungan Pengembangan

### Jalankan Tes

```bash
python manage.py test engine_module modules.product_module
```

### Linting

```bash
flake8 .
```

### Formatter

```bash
black .
```

---

## 🌐 Environment Produksi

1. Set `DEBUG = False`
2. Gunakan Nginx/Apache
3. Gunakan WSGI server (Gunicorn/uWSGI)
4. Atur `SECRET_KEY` via environment variable

```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

5. Aktifkan HTTPS

---

System ini di kembangkan hanya untuk test masuk kerja `Hash Micro`
