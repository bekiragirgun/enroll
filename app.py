"""
Ders Takip Sistemi — Flask Sunucusu
Kapadokya Üniversitesi Linux Dersleri

Başlatmak için:
    python3 app.py

Öğretmen paneli: http://localhost:3333/teacher
"""

import eventlet
eventlet.monkey_patch()
from eventlet.debug import hub_prevent_multiple_readers
hub_prevent_multiple_readers(False)

import os
import pty
import subprocess
import signal
import threading
from flask import Flask, session, request, Response
from flask_socketio import SocketIO, emit
import sys
import argparse

# ── Import Core and Routes ──────────────────────────────────────────
from core.db import db_olustur
from core.config import ayarlari_yukle, ders_durumu
import logging
import collections

from routes.student import student_bp
from routes.teacher import teacher_bp
from routes.api import api_bp
from routes.terminal import terminal_bp
from routes.exam import exam_bp

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'kapadokya-linux-2024')

# ── In-memory log buffer (UI için) ────────────────────────────
log_buffer = collections.deque(maxlen=500)  # Son 500 log satırı

class _BufHandler(logging.Handler):
    """Her log kaydını log_buffer'a ekler."""
    def emit(self, record):
        try:
            log_buffer.append({
                'ts': int(record.created * 1000),  # ms cinsinden timestamp
                'seviye': record.levelname,
                'mesaj': self.format(record),
            })
        except Exception:
            pass

# ── Uygulama ──────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Static dosyaları cache'leme
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # HTTP üzerinden çalışıyoruz
log = app.logger
log.setLevel(logging.INFO)

# BufHandler'ı kök logger'a ekle — tüm modüllerin log.info/error'ları yakalanır
_buf_handler = _BufHandler()
_buf_handler.setFormatter(logging.Formatter('%(name)s — %(message)s'))
logging.getLogger().addHandler(_buf_handler)

# eventlet ile daha performanslı ve stabil WebSocket desteği
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

@app.route('/slayt/<path:filename>')
def serve_slayt(filename):
    from flask import send_from_directory
    from core.config import ders_durumu
    
    klasor = ders_durumu.get('slayt_klasoru', '')
    if not klasor or not os.path.exists(klasor):
        return "Slayt klasörü bulunamadı", 404
        
    return send_from_directory(klasor, filename)

@app.route('/gorseller/<path:filename>')
def serve_gorseller(filename):
    from flask import send_from_directory
    from core.paths import GORSELLER_DIR
    return send_from_directory(GORSELLER_DIR, filename)

# ── Blueprints ──────────────────────────────────────────────
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(api_bp)
app.register_blueprint(terminal_bp)
app.register_blueprint(exam_bp)

# İlk yükleme
db_olustur()
ayarlari_yukle()


# ── SocketIO Terminal Olayları ────────────────────────────────
ogrenci_surecleri = {}  # {sid: (process, master_fd)}
ogrenci_sidleri   = {}  # {sid: username}
ogrenci_pty_locks = {}  # {fd: threading.Lock()}

ogretmen_pty_fd   = None
ogretmen_pty_pid  = None
ogretmen_pty_lock = threading.Lock()
ogretmen_sid = None
ogretmen_komut_tampon = ""
_ogretmen_pty_kapaniyor = False  # Eski PTY'nin kapandığını reader thread'e bildir
ogretmen_izlenen_sid = None  # Öğretmenin şu an izlediği öğrenci SID'i
ogretmen_mudahale = False     # Müdahale modu açık mı

# Blueprint'lerin aynı dict/deque nesnelerini görmesi için core.state'e bağla
# (double-import tuzağını önler: app.py __main__ olarak çalışır)
import core.state as _state
_state.ogrenci_surecleri = ogrenci_surecleri
_state.ogrenci_sidleri   = ogrenci_sidleri
_state.ogrenci_pty_locks = ogrenci_pty_locks
_state.log_buffer        = log_buffer

def _pty_oku_ve_yayinla(fd, hedef_event, hedef_room=None, broadcast=False):
    """PTY fd'den oku ve SocketIO üzerinden yayınla.

    fd kapandığında veya hata oluştuğunda sessizce çıkar.
    """
    import select
    while True:
        try:
            # select ile bekle - fd kapanırsa hemen çıkar
            ready, _, _ = select.select([fd], [], [], 1.0)
            if not ready:
                continue
            data = os.read(fd, 4096)
            if not data:
                break
            text = data.decode('utf-8', errors='replace')
            if broadcast:
                socketio.emit(hedef_event, text, namespace='/terminal')
            elif hedef_room:
                socketio.emit(hedef_event, text, room=hedef_room, namespace='/terminal')
                # İzleme relay: Eğer bu fd izlenen öğrenciye aitse, öğretmene de gönder
                if ogretmen_izlenen_sid and hedef_room == ogretmen_izlenen_sid and ogretmen_sid:
                    socketio.emit('izleme_cikti', text, room=ogretmen_sid, namespace='/terminal')
        except (OSError, IOError, EOFError, ValueError):
            break
        except Exception as e:
            log.error(f"PTY Okuma hatası: {e}")
            break

@socketio.on('connect', namespace='/terminal')
def terminal_baglan():
    pass

@socketio.on('ogrenci_heartbeat', namespace='/terminal')
def handle_heartbeat(data):
    numara = data.get('numara')
    if not numara: return
    
    from core.db import db_baglantisi, DBWrapper
    from core.utils import bugun, simdi
    
    try:
        with db_baglantisi() as conn:
            db = DBWrapper(conn)
            db.execute("""
                INSERT INTO ogrenci_aktivite_log (numara, ip, aktivite_tipi, detay, tarih, saat)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                numara,
                request.remote_addr,
                'heartbeat',
                f"Mod: {data.get('mod')}, Slayt: {data.get('slayt')}, Durum: {data.get('durum')}",
                bugun(),
                simdi()
            ))
            db.commit()
    except Exception as e:
        app.logger.error(f"Heartbeat log hatası: {e}")

@socketio.on('disconnect', namespace='/terminal')
def terminal_kopma(*args):
    global ogretmen_sid, ogretmen_pty_fd, ogretmen_pty_pid
    sid = request.sid

    if sid == ogretmen_sid:
        if ogretmen_pty_pid:
            try: os.kill(ogretmen_pty_pid, signal.SIGHUP)
            except ProcessLookupError: pass
        ogretmen_sid = None
        ogretmen_pty_fd = None
        ogretmen_pty_pid = None
        return

    if sid in ogrenci_sidleri:
        ogrenci_sidleri.pop(sid, None)
        if sid in ogrenci_surecleri:
            proc, fd = ogrenci_surecleri.pop(sid)
            ogrenci_pty_locks.pop(fd, None)
            try: os.close(fd)
            except OSError: pass
            try: os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:
                try: proc.terminate()
                except: pass
        if ogretmen_sid:
            socketio.emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri), room=ogretmen_sid, namespace='/terminal')

@socketio.on('ogretmen_baglan', namespace='/terminal')
def ogretmen_baglan_event(veri=None):
    global ogretmen_sid, ogretmen_pty_fd, ogretmen_pty_pid, ders_durumu
    ogretmen_sid = request.sid
    ogretmen_numara = 'ogretmen'

    # Eski PTY'yi temizle - önce process'i öldür, sonra fd'yi kapat
    # fd kapatılınca reader thread otomatik çıkar (select/read hata verir)
    eski_fd = ogretmen_pty_fd
    eski_pid = ogretmen_pty_pid
    ogretmen_pty_fd = None
    ogretmen_pty_pid = None

    if eski_pid:
        try: os.killpg(os.getpgid(eski_pid), signal.SIGTERM)
        except ProcessLookupError: pass
        except Exception: pass
    if eski_fd is not None:
        try: os.close(eski_fd)
        except OSError: pass
        import time
        time.sleep(0.3)  # Reader thread'in çıkmasını bekle

    from chroot_terminal import chroot_var_mi, chroot_olustur, CHROOT_HOST, CHROOT_REAL_SSH_PORT, CHROOT_USER, CHROOT_PASS, CHROOT_BASE, _slugify
    ogretmen_numara = _slugify(ogretmen_numara)

    try:
        if not chroot_var_mi(ogretmen_numara):
            log.info(f"Öğretmen chroot ortamı oluşturuluyor...")
            chroot_olustur(ogretmen_numara, "Öğretmen", "Paneli")

        master_fd, slave_fd = pty.openpty()
        safe_username = ogretmen_numara.replace("'", "'\\''")
        safe_chroot_path = f"{CHROOT_BASE}/{safe_username}".replace("'", "'\\''")

        ssh_cmd = [
            'ssh', '-t',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'ControlPath=none',
            '-p', str(CHROOT_REAL_SSH_PORT),
            f'{CHROOT_USER}@{CHROOT_HOST}',
            f"sudo /bin/bash -c \"while true; do chroot '{safe_chroot_path}' /bin/su - '{safe_username}'; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\""
        ]
        if CHROOT_PASS:
            ssh_cmd = ['sshpass', '-p', CHROOT_PASS] + ssh_cmd

        proc = subprocess.Popen(ssh_cmd, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)
        os.close(slave_fd)

        ogretmen_pty_fd = master_fd
        ogretmen_pty_pid = proc.pid

        t = threading.Thread(target=_pty_oku_ve_yayinla, args=(master_fd, 'ogretmen_cikti', None, True), daemon=True)
        t.start()

        emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri))

    except Exception as e:
        log.error(f"Öğretmen terminal bağlantı hatası: {str(e)}")
        emit('hata', f'Terminal bağlantı hatası: {str(e)}')

@socketio.on('ogretmen_girdi', namespace='/terminal')
def ogretmen_girdi_event(veri):
    global ogretmen_pty_fd, ogretmen_komut_tampon
    char = veri.get('data', '')
    
    if ogretmen_pty_fd is not None:
        with ogretmen_pty_lock:
            try: os.write(ogretmen_pty_fd, char.encode('utf-8'))
            except OSError: pass

    if char == '\r' or char == '\n':
        if ogretmen_komut_tampon.strip():
            socketio.emit('ogretmen_komut', ogretmen_komut_tampon.strip(), namespace='/terminal')
        ogretmen_komut_tampon = ""
    elif char == '\x7f' or char == '\x08': # Backspace
        ogretmen_komut_tampon = ogretmen_komut_tampon[:-1]
    elif len(char) == 1 and char.isprintable():
        ogretmen_komut_tampon += char

@socketio.on('ogretmen_temizle', namespace='/terminal')
def ogretmen_temizle_event():
    socketio.emit('ogretmen_temizle', namespace='/terminal')

@socketio.on('ogretmen_izle', namespace='/terminal')
def ogretmen_izle_event(veri):
    global ogretmen_izlenen_sid, ogretmen_mudahale
    if request.sid != ogretmen_sid:
        return

    username = veri.get('username', '')
    # SID'i bul
    hedef_sid = None
    for sid, uname in ogrenci_sidleri.items():
        if uname == username:
            hedef_sid = sid
            break

    if not hedef_sid or hedef_sid not in ogrenci_surecleri:
        emit('izleme_hata', 'Bu öğrencinin aktif terminali yok')
        return

    ogretmen_izlenen_sid = hedef_sid
    ogretmen_mudahale = False
    emit('izleme_basladi', {'username': username, 'sid': hedef_sid})
    log.info(f"Öğretmen izleme başladı: {username}")

@socketio.on('ogretmen_izle_girdi', namespace='/terminal')
def ogretmen_izle_girdi_event(veri):
    global ogretmen_mudahale
    if request.sid != ogretmen_sid or not ogretmen_izlenen_sid:
        return
    if not ogretmen_mudahale:
        return  # Read-only modda yazma yok

    if ogretmen_izlenen_sid in ogrenci_surecleri:
        _, fd = ogrenci_surecleri[ogretmen_izlenen_sid]
        lock = ogrenci_pty_locks.get(fd)
        data = veri.get('data', '')
        if lock:
            with lock:
                try: os.write(fd, data.encode('utf-8'))
                except OSError: pass
        else:
            try: os.write(fd, data.encode('utf-8'))
            except OSError: pass

@socketio.on('ogretmen_izle_birak', namespace='/terminal')
def ogretmen_izle_birak_event():
    global ogretmen_izlenen_sid, ogretmen_mudahale
    if request.sid != ogretmen_sid:
        return
    log.info(f"Öğretmen izleme bıraktı")
    ogretmen_izlenen_sid = None
    ogretmen_mudahale = False

@socketio.on('ogretmen_mudahale_toggle', namespace='/terminal')
def ogretmen_mudahale_toggle_event(veri):
    global ogretmen_mudahale
    if request.sid != ogretmen_sid:
        return
    ogretmen_mudahale = veri.get('aktif', False)
    log.info(f"Öğretmen müdahale modu: {'açık' if ogretmen_mudahale else 'kapalı'}")

@socketio.on('ogrenci_baglan', namespace='/terminal')
def ogrenci_baglan_event(veri):
    sid = request.sid
    username = veri.get('username', '')

    if not username:
        emit('hata', 'Kullanıcı adı gerekli!')
        return

    if sid in ogrenci_surecleri:
        proc, fd = ogrenci_surecleri.pop(sid)
        try: os.close(fd)
        except: pass
        try: os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except: pass

    ogrenci_sidleri[sid] = username
    try:
        from chroot_terminal import CHROOT_HOST, CHROOT_REAL_SSH_PORT, CHROOT_USER, CHROOT_PASS, CHROOT_BASE, _slugify, chroot_olustur
        username = _slugify(username)
        
        ad_soyad = "Ogrenci"
        from core.db import db_baglantisi
        with db_baglantisi() as db:
            row = db.execute("SELECT ad, soyad FROM ogrenciler WHERE numara=?", (username,)).fetchone()
            if row: ad_soyad = f"{row['ad']} {row['soyad']}"
            elif username.startswith('u') and username[1:].isdigit():
                row = db.execute("SELECT ad, soyad FROM ogrenciler WHERE numara=?", (username[1:],)).fetchone()
                if row: ad_soyad = f"{row['ad']} {row['soyad']}"

        chroot_olustur(username, ad_soyad, "") 

        master_fd, slave_fd = pty.openpty()
        safe_username = username.replace("'", "'\\''")
        safe_chroot_path = f"{CHROOT_BASE}/{safe_username}".replace("'", "'\\''")
        ssh_cmd = [
            'ssh', '-t',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'ControlPath=none',
            '-p', str(CHROOT_REAL_SSH_PORT), f'{CHROOT_USER}@{CHROOT_HOST}',
            f"sudo /bin/bash -c \"while true; do chroot '{safe_chroot_path}' /bin/su - '{safe_username}'; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\""
        ]
        if CHROOT_PASS:
            ssh_cmd = ['sshpass', '-p', CHROOT_PASS] + ssh_cmd

        proc = subprocess.Popen(ssh_cmd, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)
        os.close(slave_fd)

        ogrenci_surecleri[sid] = (proc, master_fd)
        ogrenci_pty_locks[master_fd] = threading.Lock()

        socketio.emit('container_hazir', room=sid, namespace='/terminal')

        t = threading.Thread(target=_pty_oku_ve_yayinla, args=(master_fd, 'terminal_cikti', sid), daemon=True)
        t.start()

    except Exception as e:
        log.error(f"[Socket] Terminal bağlantı hatası: {str(e)}")
        socketio.emit('hata', f'Terminal bağlantı hatası: {str(e)}', room=sid, namespace='/terminal')

@socketio.on('terminal_girdi', namespace='/terminal')
def ogrenci_girdi_event(veri):
    sid = request.sid
    if sid in ogrenci_surecleri:
        _, fd = ogrenci_surecleri[sid]
        try:
            os.write(fd, veri['data'].encode('utf-8'))
        except OSError:
            pass


# ── HTTPS bağlantılarını zararsız şekilde kapat ─────────────


# ── Başlat ────────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse
    import socket
    import os # Added this import as it's used in the new block
    
    parser = argparse.ArgumentParser(description='Ders Takip Sistemi')
    parser.add_argument('--test', action='store_true', help='Test modunda başlat (SQLite + Örnek Veri)')
    parser.add_argument('--port', type=int, default=3333, help='Dinlenecek port')
    args = parser.parse_args()

    # Moved db_olustur and related imports here
    import core.db
    from core.db import db_olustur

    if args.test:
        print("\n" + "="*55)
        print("  🚀 TEST MODU AKTİF")
        print("  📂 Veritabanı: SQLite")
        print("  👥 Örnek veriler yükleniyor...")
        print("="*55 + "\n")
        
        os.environ['DB_TYPE'] = 'sqlite'
        from core.db import test_verilerini_yukle
        db_olustur()
        test_verilerini_yukle()
    else:
        db_olustur()

    # IP Tespiti
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        yerel_ip = s.getsockname()[0]
        s.close()
    except Exception:
        yerel_ip = '127.0.0.1'

    print('\n' + '=' * 55)
    print('  🐧 Ders Takip Sistemi başlatıldı!')
    print('=' * 55)
    print(f'  Öğrenciler için    : http://{yerel_ip}:{args.port}')
    print(f'  Öğretmen paneli    : http://localhost:{args.port}/teacher')
    print(f'  Sistem IP          : 🛠️ {yerel_ip}')
    print('=' * 55 + '\n')

    from chroot_terminal import CHROOT_HOST, CHROOT_REAL_SSH_PORT, _is_local
    is_local = _is_local(CHROOT_HOST)
    mode_text = "🏠 LOCAL MODE" if is_local else "🌐 REMOTE MODE"
    print(f'  Chroot Host (991)  : ✅ {CHROOT_HOST}:{CHROOT_REAL_SSH_PORT} ({mode_text})')
    print(f'  Sistem IP          : 🛠️ {yerel_ip}')
    print('=' * 55 + '\n')

    socketio.run(app, host='0.0.0.0', port=args.port, debug=True) # Modified to use args.port and debug=True
