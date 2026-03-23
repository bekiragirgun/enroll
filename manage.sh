#!/bin/bash
# Ders Takip Sistemi - Uygulama Başlatma Wrapper Scripti

cd "$(dirname "$0")"

echo "================================================="
echo "   Kapadokya Üniversitesi - Ders Takip Sistemi   "
echo "================================================="

# 1. Öncelikle yerel 'venv' klasörü var mı kontrol et
if [ -f "venv/bin/activate" ]; then
    echo "📦 Yerel Python sanal ortamı (venv) aktifleştiriliyor..."
    source venv/bin/activate

# 2. Yoksa, sistemdeki conda ile 'kapadokya-DT' yi ara
elif command -v conda &> /dev/null; then
    CONDA_BASE=$(conda info --base)
    if [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
        source "$CONDA_BASE/etc/profile.d/conda.sh"
        if conda info --envs | awk '{print $1}' | grep -qx "kapadokya-DT"; then
            echo "✅ 'kapadokya-DT' Conda ortamı aktifleştiriliyor..."
            conda activate kapadokya-DT
        else
            echo "⚠️ 'kapadokya-DT' conda ortamı veya 'venv' bulunamadı!"
            echo "Sistemdeki varsayılan Python sürümü kullanılacak."
            echo "Tavsiye: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
            echo "-------------------------------------------------"
        fi
    fi
fi

echo "🚀 Uygulama başlatılıyor (app.py) ..."
exec python3 app.py "$@"
