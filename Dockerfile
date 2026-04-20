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

# SSH client optimizasyonu (Docker↔Parallels VM latency için)
# - ControlMaster: Tek TCP+SSH bağlantıyı multiplexle; 30 öğrencinin sonraki
#   handshake'leri ~50ms'e düşer.
# - chacha20-poly1305: LAN için AES-256'dan daha hızlı.
# - UseDNS/Compression zaten kapalı (VM tarafında). Client'ta da ekleyelim.
RUN mkdir -p /home/appuser/.ssh && \
    printf 'Host *\n\
    ControlMaster auto\n\
    ControlPath /tmp/ssh-mux-%%r@%%h:%%p\n\
    ControlPersist 10m\n\
    ServerAliveInterval 30\n\
    ServerAliveCountMax 3\n\
    Ciphers chacha20-poly1305@openssh.com,aes128-gcm@openssh.com,aes256-gcm@openssh.com\n\
    MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-256\n\
    KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org\n\
    Compression no\n\
    TCPKeepAlive yes\n\
    StrictHostKeyChecking accept-new\n\
    UserKnownHostsFile /tmp/known_hosts\n' > /home/appuser/.ssh/config && \
    chmod 600 /home/appuser/.ssh/config && \
    chown -R appuser:appuser /home/appuser/.ssh

# Flask portu
EXPOSE 3333

# Uygulamayı başlat (app.py içindeki config'e göre)
USER appuser
CMD ["python", "app.py"]
