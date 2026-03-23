#!/bin/bash

# migrate.sh — Docker ve PostgreSQL Taşıma Otomasyonu

echo "🐘 PostgreSQL ve Docker ortamı başlatılıyor..."

# Docker Compose'u arka planda başlat
docker-compose up -d db

# Veritabanının hazır olmasını bekle (PostgreSQL portunu kontrol et)
echo "⏳ Veritabanının hazır olması bekleniyor (60 saniye boyunca denenecek)..."
MAX_RETRIES=12
RETRY_COUNT=0
while ! docker exec $(docker-compose ps -q db) pg_isready -h localhost -U postgres > /dev/null 2>&1; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "❌ Hata: PostgreSQL zamanında hazır olmadı."
        exit 1
    fi
    echo "   ($RETRY_COUNT/$MAX_RETRIES) Bekleniyor..."
    sleep 5
done

echo "✅ PostgreSQL hazır. Veri taşıma işlemi başlatılıyor..."

# Python taşıma betiğini çalıştır
# Conda ortamını kullanarak çalıştırıyoruz
conda run -n kapadokya-DT python3 migrate_to_pg.py

if [ $? -eq 0 ]; then
    echo "✨ Taşıma başarıyla tamamlandı!"
    echo "🚀 Şimdi tüm sistemi 'docker-compose up -d' ile tam kapasite başlatabilirsiniz."
else
    echo "❌ Taşıma sırasında bir hata oluştu. Lütfen logları kontrol edin."
    exit 1
fi
