"""
Ders Takip Sistemi — Flask Sunucusu
Kapadokya Üniversitesi Linux Dersleri

Başlatmak için:
    python3 app.py

Öğretmen paneli: http://localhost:3333/teacher
"""

# ─── FD limit (CRITICAL — eventlet.monkey_patch ÖNCESİ) ──────────
# macOS'ta zsh "unlimited" göstermesine rağmen BSD heritage'tan ötürü
# kernel default hard limit OPEN_MAX = 10240 — buna ulaşınca [Errno 24]
# Too many open files. Her öğrenci ~5 FD (websocket + PTY pair + SSH
# pipe), 30 öğrenci × 5 + DB pool + log + listening socket → 200+ FD
# kolayca. Explicit setrlimit ile kernel'e gerçek isteğimizi söylüyoruz;
# kern.maxfilesperproc (~184k) altına kadar yükseltilir.
import resource as _resource
import sys as _sys
try:
    _soft, _hard = _resource.getrlimit(_resource.RLIMIT_NOFILE)
    _target = 65536
    # Hard limit RLIM_INFINITY (max int64) ise dokunmaya gerek yok;
    # gerçek bir sayıysa onun altında kalmamız şart (process kendi
    # hard'ını yükseltemez). soft <= hard zorunluluğu için min al.
    _new_soft = min(_target, _hard) if _hard > 0 else _target
    _resource.setrlimit(_resource.RLIMIT_NOFILE, (_new_soft, _hard))
    _soft2, _hard2 = _resource.getrlimit(_resource.RLIMIT_NOFILE)
    print(f"📂 FD limiti: soft={_soft2}, hard={_hard2}", flush=True)
except (ValueError, OSError) as _e:
    print(f"⚠️  FD limit yükseltilemedi: {_e}", flush=True)

import eventlet
eventlet.monkey_patch()
from eventlet.debug import hub_prevent_multiple_readers
hub_prevent_multiple_readers(False)

# psycogreen — psycopg2 bağlantılarının eventlet greenlet'leri ile uyumlu
# çalışmasını sağlar. Olmadan: PG auth sırasında greenlet yield edemez →
# "canceling authentication due to timeout" hatası + CPU %99 loop.
try:
    from psycogreen.eventlet import patch_psycopg
    patch_psycopg()
except ImportError:
    # psycogreen yüklü değilse uyar ama başlamayı engelleme
    import sys
    print("⚠️  psycogreen yüklü değil — PG auth timeout riski var", file=sys.stderr)

import os
import pty
import subprocess
import signal
import shlex
import threading
from flask import Flask, session, request, Response, g
from flask_socketio import SocketIO, emit
from flask_wtf.csrf import CSRFProtect
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

secret = os.environ.get('SECRET_KEY')
if not secret:
    import secrets as _s
    secret = _s.token_hex(32)
    print("⚠️ SECRET_KEY environment variable ayarlanmamış! Geçici key üretildi.")
SECRET_KEY = secret

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
# CSRF token süresi — default 1 saat, ders günü 8+ saat sürüyor.
# Öğrenci giriş sayfasını açıp beklerse token expire olmasın.
app.config['WTF_CSRF_TIME_LIMIT'] = None  # Token session boyunca geçerli
log = app.logger
log.setLevel(logging.INFO)

# BufHandler'ı kök logger'a ekle — tüm modüllerin log.info/error'ları yakalanır
_buf_handler = _BufHandler()
_buf_handler.setFormatter(logging.Formatter('%(name)s — %(message)s'))
logging.getLogger().addHandler(_buf_handler)

# eventlet ile daha performanslı ve stabil WebSocket desteği
socketio = SocketIO(app, cors_allowed_origins=[], async_mode='eventlet')
csrf = CSRFProtect(app)

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

@app.route('/slayt-kaynak/<path:filename>')
def serve_slayt_kaynak(filename):
    """SLIDE_HOST_BASE altındaki herhangi bir dosyayı serve eder.

    Slayt HTML'lerine `<base href="/slayt-kaynak/.../">` enjekte ettiğimizde,
    tarayıcı tüm relative <img src="../../06_KAYNAKLAR/...">, <img src="../gorseller/...">
    gibi URL'leri otomatik bu route'a yönlendirir.

    send_from_directory `safe_join` ile path traversal koruması sağlar.
    """
    from flask import send_from_directory
    base = os.environ.get('SLIDE_HOST_BASE', '').strip()
    if not base or not os.path.exists(base):
        return "Slayt kaynak kökü tanımsız (.env'de SLIDE_HOST_BASE eksik)", 404
    return send_from_directory(base, filename)


@app.route('/slayt/<path:filename>')
def serve_slayt(filename):
    """Slayt dosyasını serve eder. HTML ise içeriğine `<base href>` enjekte ederek
    relative görsel/CSS yollarının SLIDE_HOST_BASE'e göre çözülmesini sağlar.

    Path traversal koruması: HTML olmayan dosyalar `send_from_directory` ile
    güvenli serve edilir (Flask safe_join). HTML dosyaları için manuel okuma
    yapılırken `Path.resolve().relative_to()` ile klasör içi olduğu doğrulanır;
    `..` veya symlink ile dışarı çıkma denemeleri ValueError fırlatır.
    """
    from flask import send_from_directory, Response
    from core.config import ders_durumu
    from pathlib import Path

    klasor = ders_durumu.get('slayt_klasoru', '')
    if not klasor or not os.path.exists(klasor):
        return "Slayt klasörü bulunamadı", 404

    # HTML dışındaki dosyaları (PDF, vs.) doğrudan klasörden serve et
    if not filename.lower().endswith('.html'):
        return send_from_directory(klasor, filename)

    # Path traversal güvenliği: resolve sonrası klasör altı olduğunu doğrula
    klasor_resolved = Path(klasor).resolve()
    try:
        yol = (klasor_resolved / filename).resolve()
        yol.relative_to(klasor_resolved)  # ValueError if outside
    except (ValueError, OSError):
        app.logger.warning(f"🛡️ Path traversal denemesi engellendi: filename={filename!r}")
        return "Geçersiz yol", 403

    if not yol.exists() or not yol.is_file():
        return "Slayt bulunamadı", 404

    base = os.environ.get('SLIDE_HOST_BASE', '').strip()
    try:
        icerik = yol.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return f"Slayt okunamadı: {e}", 500

    # Base href enjekte et — slayt klasörünün SLIDE_HOST_BASE'e göre relative path'i
    if base:
        try:
            rel = Path(klasor).resolve().relative_to(Path(base).resolve())
            base_href = f"/slayt-kaynak/{rel}/" if str(rel) != '.' else "/slayt-kaynak/"
            base_tag = f'<base href="{base_href}">'
            # Mevcut <base ...> varsa dokunma; yoksa <head>'in hemen başına ekle
            lower = icerik.lower()
            if '<base ' not in lower:
                if '<head>' in lower:
                    idx = lower.find('<head>') + len('<head>')
                    icerik = icerik[:idx] + base_tag + icerik[idx:]
                elif '<html' in lower:
                    # <head> yok ama <html> var → <html ...> tag'inden sonra <head><base>
                    idx = lower.find('>', lower.find('<html')) + 1
                    icerik = icerik[:idx] + f'<head>{base_tag}</head>' + icerik[idx:]
        except ValueError:
            # Slayt klasörü base dışındaysa enjekte etme — relative yollar zaten çalışmayacak
            pass
        except Exception as e:
            app.logger.warning(f"slayt base href enjeksiyonu başarısız: {e}")

    return Response(icerik, mimetype='text/html; charset=utf-8')

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

# İlk yükleme (Artık __main__ içinde yapılıyor)


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

    V28: Basit blocking os.read — monkey_patch ile yield olur.
    """
    log.info(f"📖 Reader başladı fd={fd} event={hedef_event} broadcast={broadcast}")
    toplam = 0
    while True:
        try:
            data = os.read(fd, 4096)
            if not data:
                log.info(f"📖 Reader fd={fd} EOF — çıkılıyor (toplam {toplam} byte)")
                break
            toplam += len(data)
            text = data.decode('utf-8', errors='replace')
            if broadcast:
                socketio.emit(hedef_event, text, namespace='/terminal')
            elif hedef_room:
                socketio.emit(hedef_event, text, room=hedef_room, namespace='/terminal')
                if ogretmen_izlenen_sid and hedef_room == ogretmen_izlenen_sid and ogretmen_sid:
                    socketio.emit('izleme_cikti', text, room=ogretmen_sid, namespace='/terminal')
        except (OSError, IOError, EOFError, ValueError) as e:
            log.info(f"📖 Reader fd={fd} kapandı: {e}")
            break
        except Exception as e:
            log.error(f"❌ PTY Okuma hatası: {e}")
            break

@socketio.on('connect', namespace='/terminal')
def terminal_baglan():
    pass

@socketio.on('ogrenci_heartbeat', namespace='/terminal')
def handle_heartbeat(data):
    """Heartbeat — sadece bellekte tutulur (online listesi için).

    Eskiden her tetiklenişte ogrenci_aktivite_log'a yazılıyordu — bu DB spam
    yarattığı için kaldırıldı. Anlamlı semantik olaylar (giris/cikis/slayt_degis/
    terminal_komut) Faz B/C içinde ayrı ayrı yazılıyor.
    """
    return

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
    log.info(f"🔌 ogretmen_baglan event: sid={request.sid}, session_ogretmen={session.get('ogretmen')}")
    if not session.get('ogretmen'):
        log.warning(f"⚠️ ogretmen_baglan reddedildi — session.ogretmen yok")
        return
    global ogretmen_sid, ogretmen_pty_fd, ogretmen_pty_pid, ders_durumu
    ogretmen_sid = request.sid
    ogretmen_numara = 'ogretmen'

    # Eski PTY'yi temizle - önce process'i öldür, sonra fd'yi kapat
    # fd kapatılınca reader thread otomatik çıkar (select/read hata verir)
    eski_fd = ogretmen_pty_fd
    eski_pid = ogretmen_pty_pid
    ogretmen_pty_fd = None
    ogretmen_pty_pid = None

    log.info(f"🔎 eski_pid={eski_pid}, eski_fd={eski_fd}")
    if eski_pid:
        try: os.killpg(os.getpgid(eski_pid), signal.SIGTERM)
        except ProcessLookupError: pass
        except Exception: pass
    if eski_fd is not None:
        try: os.close(eski_fd)
        except OSError: pass
        import time
        time.sleep(0.3)  # Reader thread'in çıkmasını bekle
    log.info(f"🔎 eski PTY temizlik tamam")

    try:
        from chroot_terminal import chroot_var_mi, chroot_olustur, CHROOT_HOST, CHROOT_REAL_SSH_PORT, CHROOT_USER, CHROOT_PASS, CHROOT_BASE, _slugify
        log.info(f"🔎 chroot_terminal import OK (HOST={CHROOT_HOST}, USER={CHROOT_USER}, PASS={'yes' if CHROOT_PASS else 'NO'})")
    except Exception as ie:
        import traceback
        log.error(f"❌ chroot_terminal import hatası: {ie}")
        log.error(traceback.format_exc())
        return
    ogretmen_numara = _slugify(ogretmen_numara)

    try:
        log.info(f"🔎 chroot_var_mi({ogretmen_numara}) kontrol ediliyor...")
        var = chroot_var_mi(ogretmen_numara)
        log.info(f"🔎 chroot_var_mi sonuç: {var}")
        if not var:
            log.info(f"Öğretmen chroot ortamı oluşturuluyor...")
            chroot_olustur(ogretmen_numara, "Öğretmen", "Paneli")
            log.info(f"✅ chroot_olustur tamamlandı")

        log.info(f"🔎 pty.openpty çağrılıyor")
        master_fd, slave_fd = pty.openpty()
        log.info(f"🔎 PTY açıldı master={master_fd} slave={slave_fd}")
        safe_username = shlex.quote(ogretmen_numara)
        safe_chroot_path = shlex.quote(f"{CHROOT_BASE}/{ogretmen_numara}")

        ssh_cmd = [
            'ssh', '-t',
            '-o', 'StrictHostKeyChecking=accept-new',
            # V26: ControlPath=none kaldırıldı — ~/.ssh/config'deki ControlMaster
            # multiplexing devrede. İlk bağlantı master açar, sonrakiler aynı
            # TCP+SSH kanalını paylaşır (30 öğrenci × handshake yerine ~1 handshake).
            '-p', f'{CHROOT_REAL_SSH_PORT}',
            f'{CHROOT_USER}@{CHROOT_HOST}',
            # V26: chroot öncesi mount — snapshot revert ya da ilk boot'ta
            # /dev/pts, /proc, /sys bind-mount'ları eksikse PTY allocation fail
            # eder. chroot-yonetici mount idempotenttir.
            f"sudo /usr/local/bin/chroot-yonetici mount {safe_username} >/dev/null 2>&1; "
            f"sudo /bin/bash -c \"while true; do chroot {safe_chroot_path} /usr/bin/su - {safe_username}; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\""
        ]
        if CHROOT_PASS:
            ssh_cmd = ['sshpass', '-p', CHROOT_PASS] + ssh_cmd
            log.info(f"🔎 sshpass ile ssh spawn ediliyor (PASS set)")
        else:
            log.info(f"🔎 sshpass'siz ssh spawn ediliyor (PASS YOK!)")

        proc = subprocess.Popen(ssh_cmd, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)
        log.info(f"🔎 subprocess.Popen başarılı PID={proc.pid}")
        os.close(slave_fd)

        ogretmen_pty_fd = master_fd
        ogretmen_pty_pid = proc.pid

        t = threading.Thread(target=_pty_oku_ve_yayinla, args=(master_fd, 'ogretmen_cikti', None, True), daemon=True)
        t.start()
        log.info(f"🔎 Reader thread başlatıldı")

        emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri))

    except Exception as e:
        import traceback
        log.error(f"❌ Öğretmen terminal bağlantı hatası: {str(e)}")
        log.error(traceback.format_exc())
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

def _ogrenci_session_temizle(username=None, skip_sid=None):
    """V28: Aynı kullanıcıya ait ESKİ PTY/process/reader greenlet'lerini kapat.

    F5 ya da WebSocket timeout disconnect tetiklemediğinde, her yeni bağlantı
    eski reader greenlet'i leak ediyordu. Bu temizleyici:
      - username veriliyse o kullanıcının tüm eski sid'lerini bulur
      - username yoksa subprocess'i ölmüş tüm session'ları toplar (reaper)
    """
    temizlenen = 0
    for old_sid in list(ogrenci_sidleri.keys()):
        if old_sid == skip_sid:
            continue
        old_username = ogrenci_sidleri.get(old_sid)
        hedef_mi = False
        if username is not None:
            # Aynı user için yeni login — eskileri nuke et
            if old_username == username:
                hedef_mi = True
        else:
            # Reaper: subprocess ölmüşse kapat
            proc_tuple = ogrenci_surecleri.get(old_sid)
            if proc_tuple:
                proc, _ = proc_tuple
                if proc.poll() is not None:  # subprocess exit
                    hedef_mi = True
            else:
                hedef_mi = True  # Process yoksa da sid'i temizle

        if not hedef_mi:
            continue

        ogrenci_sidleri.pop(old_sid, None)
        proc_tuple = ogrenci_surecleri.pop(old_sid, None)
        if proc_tuple:
            proc, fd = proc_tuple
            ogrenci_pty_locks.pop(fd, None)
            try: os.close(fd)
            except OSError: pass
            try: os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:
                try: proc.terminate()
                except Exception: pass
        temizlenen += 1
    if temizlenen:
        log.info(f"🧹 {temizlenen} eski öğrenci session'ı temizlendi (user={username})")
    return temizlenen


@socketio.on('ogrenci_baglan', namespace='/terminal')
def ogrenci_baglan_event(veri):
    log.info(f"🔌 ogrenci_baglan event: sid={request.sid}, session_numara={session.get('numara')}, veri={veri}")
    if not session.get('numara'):
        log.warning(f"⚠️ ogrenci_baglan reddedildi — session.numara yok")
        return
    sid = request.sid
    username = veri.get('username', '')

    if not username:
        emit('hata', 'Kullanıcı adı gerekli!')
        return

    # V28: Current sid temizliği (nadir: aynı sid yeniden baglan diyorsa)
    if sid in ogrenci_surecleri:
        proc, fd = ogrenci_surecleri.pop(sid)
        ogrenci_pty_locks.pop(fd, None)
        try: os.close(fd)
        except: pass
        try: os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except: pass

    # V28: Aynı username için eski sid'leri de kapat — F5 / reconnect leak fix.
    # Inline call os.killpg'de hang yapabiliyor, bu yüzden greenlet'e spawn et
    # (fire-and-forget). 60 sn'lik reaper yedek güvence.
    try:
        eventlet.spawn_n(_ogrenci_session_temizle, username, sid)
    except Exception as _e:
        log.warning(f"session temizle spawn hata: {_e}")

    ogrenci_sidleri[sid] = username
    try:
        from chroot_terminal import CHROOT_HOST, CHROOT_REAL_SSH_PORT, CHROOT_USER, CHROOT_PASS, CHROOT_BASE, _slugify, chroot_olustur
        import re
        username = _slugify(username)
        
        # Strict Input Validation: Sadece alfanumerik ve alt çizgiye izin ver
        if not re.match(r'^[a-z0-9_]+$', username):
            log.warning(f"⚠️ Geçersiz kullanıcı adı denemesi engellendi: {username}")
            emit('hata', 'Geçersiz kullanıcı adı formatı!')
            return
        
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
        safe_username = shlex.quote(username)
        safe_chroot_path = shlex.quote(f"{CHROOT_BASE}/{username}")

        ssh_cmd = [
            'ssh', '-t',
            '-o', 'StrictHostKeyChecking=accept-new',
            # V26: ControlPath=none kaldırıldı — ControlMaster multiplexing aktif.
            '-p', str(CHROOT_REAL_SSH_PORT), f'{CHROOT_USER}@{CHROOT_HOST}',
            # V26: chroot öncesi mount — idempotent, PTY allocation için şart.
            f"sudo /usr/local/bin/chroot-yonetici mount {safe_username} >/dev/null 2>&1; "
            f"sudo /bin/bash -c \"while true; do chroot {safe_chroot_path} /usr/bin/su - {safe_username}; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\""
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
    parser.add_argument('--host', type=str, help='Chroot Host IP (Örn: 10.211.55.27)')
    parser.add_argument('--user', type=str, help='Chroot SSH Kullanıcısı (Örn: bekir)')
    parser.add_argument('--pass', dest='password', type=str, help='Chroot SSH Şifresi')
    parser.add_argument('--student', type=int, default=0, help='Test öğrenci sayısı (Örn: --student 30)')
    args = parser.parse_args()

    # ── Otomatik DB Backup (her başlatmada) ──────────────────
    if not args.test:
        from pathlib import Path
        import shutil
        from datetime import datetime
        db_path = Path(__file__).parent / 'data' / 'yoklama.db'
        if db_path.exists() and db_path.stat().st_size > 0:
            backup_dir = Path(__file__).parent / 'data' / 'backups'
            backup_dir.mkdir(exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = backup_dir / f'yoklama_{ts}.db'
            shutil.copy2(db_path, backup_path)
            # Son 10 backup'ı tut, eskileri sil
            backups = sorted(backup_dir.glob('yoklama_*.db'))
            for old in backups[:-10]:
                old.unlink()
            print(f'  💾 DB backup: {backup_path.name} ({len(backups)} backup mevcut)')

    # CLI Argümanlarını Environment Variable olarak ata (config.py tarafından okunması için)
    if args.host:
        os.environ['CHROOT_HOST'] = args.host
        if not args.user or not args.password:
            print("  ⚠️ UYARI: --host verildi ama --user ve/veya --pass eksik!")
            print("  ⚠️ Chroot terminal çalışmayacak. Örnek: --host 10.211.55.28 --user bekir --pass 123123")
    if args.user:
        os.environ['CHROOT_USER'] = args.user
    if args.password:
        os.environ['CHROOT_PASS'] = args.password

    # Moved db_olustur and related imports here
    import core.db
    from core.db import db_olustur

    if args.test:
        print("\n" + "="*55)
        print("  🚀 TEST MODU AKTİF")
        print("  📂 Veritabanı: SQLite (TEMİZ BAŞLANGIÇ)")
        print("  👥 Örnek veriler yükleniyor...")
        print("="*55 + "\n")
        
        os.environ['DB_TYPE'] = 'sqlite'
        os.environ['TEST_MODE'] = '1'
        os.environ['DERS_TAKIP_TEST'] = '1'  # ÖNCE ayarla, sonra paths import et
        import importlib
        import core.paths
        importlib.reload(core.paths)  # TEST flag ile yeniden yükle → test_yoklama.db kullanır
        # GÜVENLİK: Production DB'yi asla silme
        if 'test' not in str(core.paths.DB_YOLU):
            print(f"  ⛔ HATA: Test modu ama DB yolu production'a işaret ediyor: {core.paths.DB_YOLU}")
            print(f"  ⛔ İşlem iptal edildi. Production veritabanı korundu.")
            sys.exit(1)
        if core.paths.DB_YOLU.exists():
            try:
                core.paths.DB_YOLU.unlink()
                print(f"  ✨ Eski test veritabanı silindi: {core.paths.DB_YOLU}")
            except Exception as e:
                print(f"  ⚠️ Veritabanı silinemedi (Kilitli olabilir): {e}")

        import core.db
        from core.db import db_olustur, test_verilerini_yukle, db_baglantisi
        db_olustur()

        if args.student > 0:
            print(f"  👥 {args.student} test öğrencisi oluşturuluyor...")
            test_verilerini_yukle(args.student)

            # Chroot'ları önceden toplu oluştur
            print("  🏗️  Test chroot'ları toplu olarak oluşturuluyor (Bu biraz zaman alabilir)...")
            from chroot_terminal import chroot_olustur_batch
            with db_baglantisi() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT numara, ad, soyad FROM ogrenciler")
                ogrenciler = [{"username": r[0], "ad": r[1], "soyad": r[2]} for r in cursor.fetchall()]
            
            if ogrenciler:
                chroot_olustur_batch(ogrenciler)
                print(f"  ✅ {args.student} Test Chroot'u hazır.")
        else:
            print("  ℹ️  Öğrenci oluşturulmadı (--student N ile oluşturabilirsiniz)")
            db_olustur()

    else:
        db_olustur()
    
    from core.config import ayarlari_yukle
    ayarlari_yukle()

    # PostgresLogHandler — sistem logları app_log tablosuna yazılır.
    # db_olustur() üstte zaten çağrıldı, tablo hazır.
    try:
        from core.log_handler import kurulum_yap as log_handler_kur
        log_handler_kur(app)
    except Exception as e:
        print(f"  ⚠️  Log handler kurulamadı: {e}")

    # Pre-warm scheduler — pazartesi günleri paket saatine 10 dk kala
    # otomatik chroot batch yaratır. Test günlerinde (diğer günler) çalışmaz.
    def _pre_warm_scheduler():
        from datetime import datetime
        import urllib.request
        # Paket saatleri — 10 dk önce tetikle
        TETIK = {
            '08:50': 1,  # 1. Paket 09:00 için 10 dk erken
            '12:30': 2,  # 2. Paket 12:40
            '15:15': 3,  # 3. Paket 15:25
        }
        tetiklendi = set()  # ('2026-04-20', 1) formatında

        while True:
            try:
                eventlet.sleep(60)  # dakikada bir kontrol
                now = datetime.now()
                # Sadece pazartesi (Python Pzt=0)
                if now.weekday() != 0:
                    continue
                hhmm = now.strftime('%H:%M')
                if hhmm not in TETIK:
                    continue
                paket_no = TETIK[hhmm]
                gun_key = (now.strftime('%Y-%m-%d'), paket_no)
                if gun_key in tetiklendi:
                    continue
                tetiklendi.add(gun_key)

                # Kendi endpoint'imizi çağır — auth bypass için internal flag
                # yok, onun yerine direkt fonksiyonu çağıralım
                app.logger.info(f"🤖 Auto pre-warm — Paket {paket_no} için {hhmm}")
                try:
                    with app.test_request_context():
                        from flask import session
                        session['ogretmen'] = True  # internal call için auth bypass
                        from routes.api import api_chroot_pre_warm_paket
                        resp = api_chroot_pre_warm_paket(paket_no)
                        app.logger.info(f"🤖 Paket {paket_no} pre-warm response: {resp.status_code}")
                except Exception as e:
                    app.logger.error(f"Auto pre-warm hata (paket {paket_no}): {e}")
            except Exception as e:
                try:
                    app.logger.error(f"Pre-warm scheduler hata: {e}")
                except Exception:
                    pass

    try:
        eventlet.spawn(_pre_warm_scheduler)
        print("  🤖 Pre-warm scheduler aktif (pazartesi 08:50 / 12:30 / 15:15)")
    except Exception as e:
        print(f"  ⚠️  Pre-warm scheduler başlatılamadı: {e}")

    # Auto-kick scheduler — paket bitişinde (11:35 / 15:15 / 18:00) açık
    # kalan tüm öğrenci session'larını otomatik kapatır + chroot'ları siler.
    # Öğretmenin manuel tetiklemesini beklemez.
    def _auto_kick_scheduler():
        from datetime import datetime
        # Paket bitiş saatleri → paket string
        BITIS = {
            '11:35': '1. Paket (09:00-11:35)',
            '15:15': '2. Paket (12:40-15:15)',
            '18:00': '3. Paket (15:25-18:00)',
        }
        tetiklendi = set()

        while True:
            try:
                eventlet.sleep(60)
                now = datetime.now()
                if now.weekday() != 0:  # yalnızca pazartesi
                    continue
                hhmm = now.strftime('%H:%M')
                if hhmm not in BITIS:
                    continue
                paket = BITIS[hhmm]
                gun_key = (now.strftime('%Y-%m-%d'), paket)
                if gun_key in tetiklendi:
                    continue
                tetiklendi.add(gun_key)

                app.logger.info(f"🤖 Auto-kick — {paket} ({hhmm}) bitti, session'lar kapatılıyor")
                try:
                    with app.test_request_context(
                        '/api/paket_sonu', method='POST', json={'paket': paket}
                    ):
                        from flask import session
                        session['ogretmen'] = True
                        from routes.api import api_paket_sonu
                        resp = api_paket_sonu()
                        app.logger.info(f"🤖 {paket} auto-kick response: {resp.status_code}")
                except Exception as e:
                    app.logger.error(f"Auto-kick hata ({paket}): {e}")
            except Exception as e:
                try:
                    app.logger.error(f"Auto-kick scheduler hata: {e}")
                except Exception:
                    pass

    try:
        eventlet.spawn(_auto_kick_scheduler)
        print("  🤖 Auto-kick scheduler aktif (pazartesi 11:35 / 15:15 / 18:00)")
    except Exception as e:
        print(f"  ⚠️  Auto-kick scheduler başlatılamadı: {e}")

    # V28: Periyodik reader reaper — 60 sn'de bir ölü PTY'leri süpürür.
    # F5 / crash / timeout disconnect kaçırıldığında leak birikmesin.
    def _ogrenci_reaper():
        while True:
            try:
                eventlet.sleep(60)
                _ogrenci_session_temizle()  # ölü subprocess'leri bul & kapat
            except Exception as e:
                try: app.logger.error(f"Reaper hata: {e}")
                except Exception: pass
    try:
        eventlet.spawn(_ogrenci_reaper)
        print("  🧹 PTY reaper aktif (60 sn periyot — ölü subprocess temizliği)")
    except Exception as e:
        print(f"  ⚠️  Reaper başlatılamadı: {e}")

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

    socketio.run(app, host='0.0.0.0', port=args.port, log_output=True, use_reloader=False)
