#!/bin/bash
# Ders Takip Sistemi - Uygulama Yönetim Scripti
# Kullanım:
#   ./manage.sh start      # Arka planda başlat (nohup)
#   ./manage.sh stop       # Durdur
#   ./manage.sh restart    # Yeniden başlat
#   ./manage.sh status     # Durum + PID + CPU
#   ./manage.sh logs       # Canlı log takibi (tail -f)
#   ./manage.sh            # Eski davranış: foreground başlat (app.py ile exec)
#   ./manage.sh --test     # app.py argümanlarıyla foreground

cd "$(dirname "$0")"

PIDFILE="/tmp/ders_takip.pid"
LOGFILE="logs/app.log"
mkdir -p logs

# ─── Python yürütücü seçimi ────────────────────────────────────
# Python 3.14 + eventlet uyumsuz (asyncio hub bug → [Errno 49]).
# Conda kapadokya-DT (3.11) öncelikli, venv 3.11-3.13 kabul.
pick_python() {
    for CONDA_PY in \
        "/opt/anaconda3/envs/kapadokya-DT/bin/python" \
        "/opt/miniconda3/envs/kapadokya-DT/bin/python" \
        "$HOME/anaconda3/envs/kapadokya-DT/bin/python" \
        "$HOME/miniconda3/envs/kapadokya-DT/bin/python"; do
        if [ -x "$CONDA_PY" ]; then
            echo "$CONDA_PY"
            return
        fi
    done
    if [ -x "venv/bin/python" ]; then
        VENV_PY_VER=$(venv/bin/python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
        if [ "$VENV_PY_VER" = "3.11" ] || [ "$VENV_PY_VER" = "3.12" ] || [ "$VENV_PY_VER" = "3.13" ]; then
            echo "venv/bin/python"
            return
        fi
    fi
    echo "python3"
}

# Process bul: hem pidfile hem pgrep
find_app_pid() {
    if [ -f "$PIDFILE" ]; then
        local p
        p=$(cat "$PIDFILE" 2>/dev/null)
        if [ -n "$p" ] && kill -0 "$p" 2>/dev/null; then
            echo "$p"
            return
        fi
        rm -f "$PIDFILE"
    fi
    pgrep -f "python.*[/ ]app\.py" | head -1
}

cmd_start() {
    local existing
    existing=$(find_app_pid)
    if [ -n "$existing" ]; then
        echo "⚠️  Zaten çalışıyor — PID $existing"
        echo "   Durdurmak için: ./manage.sh stop"
        exit 1
    fi

    local PYTHON_BIN
    PYTHON_BIN=$(pick_python)
    echo "✅ Python: $PYTHON_BIN"

    # Eski log'u döndür (> 5MB ise)
    if [ -f "$LOGFILE" ] && [ "$(stat -f%z "$LOGFILE" 2>/dev/null || stat -c%s "$LOGFILE" 2>/dev/null)" -gt 5242880 ]; then
        mv "$LOGFILE" "${LOGFILE}.$(date '+%Y%m%d-%H%M%S')"
        echo "📦 Eski log döndürüldü"
    fi

    nohup "$PYTHON_BIN" app.py "$@" > "$LOGFILE" 2>&1 &
    local pid=$!
    echo "$pid" > "$PIDFILE"
    echo "🚀 Başlatıldı — PID $pid"
    echo "   Log: tail -f $LOGFILE"

    # 3 sn bekle ve sağlık kontrol et
    sleep 3
    if ! kill -0 "$pid" 2>/dev/null; then
        echo "❌ Process hemen öldü — son log satırları:"
        tail -15 "$LOGFILE"
        rm -f "$PIDFILE"
        exit 1
    fi
    # /api/durum healthcheck
    for i in 1 2 3 4 5 6; do
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:3333/api/durum 2>/dev/null | grep -q "^200$"; then
            echo "✅ /api/durum 200 OK"
            return 0
        fi
        sleep 1
    done
    echo "⚠️  Process canlı ama /api/durum henüz cevap vermiyor (log'a bak)"
}

cmd_stop() {
    local pid
    pid=$(find_app_pid)
    if [ -z "$pid" ]; then
        echo "ℹ️  Çalışan process yok"
        rm -f "$PIDFILE"
        return
    fi
    echo "⏹  Durduruluyor — PID $pid"
    kill -TERM "$pid" 2>/dev/null
    for i in 1 2 3 4 5; do
        if ! kill -0 "$pid" 2>/dev/null; then
            break
        fi
        sleep 1
    done
    if kill -0 "$pid" 2>/dev/null; then
        echo "⚠️  SIGTERM'e cevap yok, SIGKILL"
        kill -9 "$pid" 2>/dev/null
    fi
    # Zombi sshpass temizliği
    pkill -9 -f "sshpass" 2>/dev/null
    rm -f /tmp/ssh-mux-* "$PIDFILE" 2>/dev/null
    echo "✅ Durduruldu"
}

cmd_restart() {
    cmd_stop
    sleep 1
    cmd_start "$@"
}

cmd_status() {
    local pid
    pid=$(find_app_pid)
    if [ -z "$pid" ]; then
        echo "⭕ Durum: DURDURULMUŞ"
        return 1
    fi
    echo "🟢 Durum: ÇALIŞIYOR — PID $pid"
    ps -p "$pid" -o pid,stat,%cpu,%mem,etime,command | tail -1
    # Health
    local health
    health=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3333/api/durum 2>/dev/null)
    echo "🏥 /api/durum: HTTP $health"
    # ssh + sshpass sayısı
    echo "🔌 sshpass: $(pgrep -f sshpass | wc -l | tr -d ' ')"
    echo "🔌 ssh→VM: $(pgrep -f 'ssh.*bekir@10' | wc -l | tr -d ' ')"
}

cmd_logs() {
    tail -f "$LOGFILE"
}

echo "================================================="
echo "   Kapadokya Üniversitesi - Ders Takip Sistemi   "
echo "================================================="

case "${1:-}" in
    start)    shift; cmd_start "$@";;
    stop)     cmd_stop;;
    restart)  shift; cmd_restart "$@";;
    status)   cmd_status;;
    logs)     cmd_logs;;
    "")
        # Eski davranış: foreground (ders sırasında hızlı dev için)
        PY=$(pick_python)
        echo "✅ Python: $PY (foreground)"
        echo "🚀 Uygulama başlatılıyor..."
        exec "$PY" app.py
        ;;
    --help|-h)
        echo "Kullanım:"
        echo "  ./manage.sh start       Arka planda başlat (nohup + pidfile)"
        echo "  ./manage.sh stop        Durdur"
        echo "  ./manage.sh restart     Yeniden başlat"
        echo "  ./manage.sh status      Durum + sağlık kontrolü"
        echo "  ./manage.sh logs        Canlı log takibi"
        echo "  ./manage.sh             Foreground çalıştır (eski davranış)"
        ;;
    *)
        # app.py'ye argüman geçme (--test, --port vs)
        PY=$(pick_python)
        echo "🚀 Uygulama başlatılıyor ($PY app.py $*)..."
        exec "$PY" app.py "$@"
        ;;
esac
