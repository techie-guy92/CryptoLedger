# ============================================================
# CryptoLedger — backend image
# Runtime settings: config.settings.prod (values come from env vars)
# Build-time collectstatic uses config.settings.collectstatic (no secrets)
# ============================================================

FROM 192.168.122.1:5000/python:3.12-slim

LABEL maintainer="soheil.dalirii@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip --timeout 120 && \
    pip install --no-cache-dir --timeout 120 --retries 5 -r requirements.txt

COPY . .

# --- Static files: build-only settings module, so no runtime secrets are needed ---
# /data is where compose keeps the SQLite file (named volume)
RUN mkdir -p /app/staticfiles /app/media /data \
    && DJANGO_SETTINGS_MODULE=config.settings.collectstatic \
       python manage.py collectstatic --noinput

RUN adduser --uid 1000 --disabled-password --gecos '' webuser && \
    chown -R webuser:webuser /app /data && \
    chmod -R 755 /app

USER webuser

EXPOSE 8000

CMD ["gunicorn", "config.asgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
