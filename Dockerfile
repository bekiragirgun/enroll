FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları
# - gcc, libpq-dev: psycopg2 derlemesi
# - sshpass, openssh-client: /api/healthcheck ve chroot_terminal.py SSH bağlantıları
# - rsync: chroot template senkronizasyonu için (chroot_yonetici de çağırabilir)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    sshpass \
    openssh-client \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Non-root user
RUN useradd -m appuser

# Flask portu
EXPOSE 3333

# Uygulamayı başlat (app.py içindeki config'e göre)
USER appuser
CMD ["python", "app.py"]
