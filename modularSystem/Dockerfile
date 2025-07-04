FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles && \
  chmod -R 755 /app/staticfiles && \
  python manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["gunicorn", "modularSystem.wsgi:application", "--bind", "0.0.0.0:8000"]