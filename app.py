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

# ── Import Core and Routes ──────────────────────────────────────────
from core.db import db_olustur
from core.config import ayarlari_yukle, ders_durumu
import logging

from routes.student import student_bp
from routes.teacher import teacher_bp
from routes.api import api_bp
from routes.terminal import terminal_bp
from routes.exam import exam_bp

SECRET_KEY = 'kapadokya-linux-2024'

# ── Uygulama ──────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Static dosyaları cache'leme
log = app.logger

# eventlet ile daha performanslı ve stabil WebSocket desteği
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

@app.route('/slayt/<path:filename>')
def serve_slayt(filename):
    from flask import send_from_directory
    from core.paths import SLAYT_DIR
    return send_from_directory(SLAYT_DIR, filename)

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

    from chroot_terminal import chroot_var_mi, chroot_olustur, CT_991_HOST, CT_991_REAL_SSH_PORT, CT_991_USER, CT_991_PASS, CHROOT_BASE, _slugify
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
            '-p', str(CT_991_REAL_SSH_PORT),
            f'{CT_991_USER}@{CT_991_HOST}',
            f"sudo /bin/bash -c \"while true; do chroot '{safe_chroot_path}' /bin/su - '{safe_username}'; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\""
        ]
        if CT_991_PASS:
            ssh_cmd = ['sshpass', '-p', CT_991_PASS] + ssh_cmd

        proc = subprocess.Popen(ssh_cmd, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)
        os.close(slave_fd)

        ogretmen_pty_fd = master_fd
        ogretmen_pty_pid = proc.pid

        t = threading.Thread(target=_pty_oku_ve_yayinla, args=(master_fd, 'ogretmen_cikti', None, True), daemon=True)
        t.start()

        if ders_durumu['mod'] != 'terminal':
            log.info(f"Otomatik mod değişimi tetiklendi: {ders_durumu['mod']} -> terminal")
            ders_durumu['mod'] = 'terminal'
            if not ders_durumu.get('terminal_url'):
                ders_durumu['terminal_url'] = '/terminal'

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
        from chroot_terminal import CT_991_HOST, CT_991_REAL_SSH_PORT, CT_991_USER, CT_991_PASS, CHROOT_BASE, _slugify, chroot_olustur
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
            '-p', str(CT_991_REAL_SSH_PORT), f'{CT_991_USER}@{CT_991_HOST}',
            f"sudo /bin/bash -c \"while true; do chroot '{safe_chroot_path}' /bin/su - '{safe_username}'; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\""
        ]
        if CT_991_PASS:
            ssh_cmd = ['sshpass', '-p', CT_991_PASS] + ssh_cmd

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
        lock = ogrenci_pty_locks.get(fd)
        if lock:
            with lock:
                try: os.write(fd, veri['data'].encode('utf-8'))
                except OSError: pass
        else:
            try: os.write(fd, veri['data'].encode('utf-8'))
            except OSError: pass


# ── HTTPS bağlantılarını zararsız şekilde kapat ─────────────


# ── Başlat ────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    import socket

    # --test flag kontrolü
    # Kullanım: python app.py --test              (varsayılan IP)
    #           python app.py 10.211.55.19 --test  (IP belirtilerek)
    if '--test' in sys.argv:
        # IP adresini argümanlardan bul (--test ve app.py dışındaki ilk argüman)
        test_ip = None
        for arg in sys.argv[1:]:
            if arg != '--test' and not arg.startswith('-'):
                test_ip = arg
                break

        os.environ['DERS_TAKIP_TEST'] = '1'
        import importlib
        import core.paths
        importlib.reload(core.paths)
        import core.db
        importlib.reload(core.db)
        from core.db import db_olustur
        db_olustur()
        from tests.test_seed import seed_test_db
        seed_test_db(host_ip=test_ip) if test_ip else seed_test_db()
        ayarlari_yukle()
        print('\n  ⚠️  TEST MODU — data/test_yoklama.db kullanılıyor\n')

    if ders_durumu.get('system_host'): yerel_ip = ders_durumu['system_host']
    else:
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
    print(f'  Öğrenciler için    : http://{yerel_ip}:3333')
    print(f'  Öğretmen paneli    : http://localhost:3333/teacher')
    print(f'  Öğretmen terminal  : http://localhost:3333/teacher/terminal')

    from chroot_terminal import CT_991_HOST, CT_991_REAL_SSH_PORT, _is_local
    is_local = _is_local(CT_991_HOST)
    mode_text = "🏠 LOCAL MODE" if is_local else "🌐 REMOTE MODE"
    print(f'  Chroot Host (991)  : ✅ {CT_991_HOST}:{CT_991_REAL_SSH_PORT} ({mode_text})')
    print(f'  Sistem IP          : 🛠️ {yerel_ip}')
    print('=' * 55 + '\n')

    socketio.run(app, host='0.0.0.0', port=3333, log_output=False)
