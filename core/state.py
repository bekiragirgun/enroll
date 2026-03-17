"""
Paylaşılan terminal oturum durumu.

app.py ve blueprint'ler bu modülden import eder — double-import tuzağını önler.
Modül attribute'larını değiştirmek için: import core.state as state; state.ogretmen_sid = x
"""

ogrenci_surecleri: dict = {}   # {sid: (process, master_fd)}
ogrenci_sidleri: dict   = {}   # {sid: username}
ogrenci_pty_locks: dict = {}   # {fd: threading.Lock}

ogretmen_sid          = None   # Öğretmen socket SID
ogretmen_izlenen_sid  = None   # İzlenen öğrenci SID
ogretmen_mudahale     = False  # Müdahale modu
