"""PostgreSQL/SQLite log handler.

Python `logging` modülünden gelen kayıtları `app_log` tablosuna yazar.
Heartbeat ve gürültülü mesajlar erken filtrelenir — DB write yapılmaz.

Tasarım notları:
- Recursive log sorununu önlemek için handler içinde oluşan exception'lar
  kesinlikle log'lanmaz (sessizce yutulur). Aksi halde DB hatası → log →
  DB hatası → log → sonsuz döngü.
- Tek satır insert (buffer yok). Eventlet altında da güvenli; perf ihtiyacı
  doğarsa sonradan buffered queue'ya geçeriz.
- Flask request context varsa IP ve oturum bilgisini ekler; yoksa boş bırakır.
"""

import logging
import re

# Bu desenler mesajda geçtiğinde DB write yapılmaz (gürültü filtresi).
# Heartbeat handler'ı her saniye çalıştığı için log spam yaratır.
_GUM_FILTRE_DESENLER = (
    'heartbeat',
    'Heartbeat',
    'HEARTBEAT',
    'GET /api/durum',
    '/api/loglar',  # Log endpoint'inin kendisi log üretmesin
    '/static/',
    '/favicon.ico',
)


class PostgresLogHandler(logging.Handler):
    """Python logging → app_log tablosu. SQLite ve PostgreSQL ile çalışır."""

    def __init__(self, level=logging.INFO):
        super().__init__(level)
        self._db_baglantisi = None  # Lazy import — circular import'u önle

    def _db(self):
        if self._db_baglantisi is None:
            from core.db import db_baglantisi
            self._db_baglantisi = db_baglantisi
        return self._db_baglantisi

    def _gurultu_mu(self, message):
        for desen in _GUM_FILTRE_DESENLER:
            if desen in message:
                return True
        return False

    def _request_baglami(self):
        """Flask request context varsa IP + oturum bilgisini al."""
        try:
            from flask import request, session, has_request_context
            if has_request_context():
                ip = request.headers.get('X-Forwarded-For', request.remote_addr or '')
                kullanici = session.get('numara') or session.get('ad_soyad') or ''
                return ip, kullanici
        except Exception:
            pass
        return '', ''

    def emit(self, record):
        try:
            mesaj = self.format(record)
            if self._gurultu_mu(mesaj):
                return

            ip, kullanici = self._request_baglami()
            level = record.levelname
            logger_ad = record.name or ''

            db_baglantisi = self._db()
            with db_baglantisi() as db:
                db.execute(
                    "INSERT INTO app_log (level, logger, message, ip, kullanici) VALUES (?, ?, ?, ?, ?)",
                    (level, logger_ad, mesaj, ip, kullanici),
                )
        except Exception:
            # Asla log handler'dan exception fırlatma — sessiz yut.
            # `logging.raiseExceptions = False` ile birlikte tam koruma.
            pass


def kurulum_yap(flask_app):
    """app.py boot sırasında çağrılır. Handler'ı flask logger'ına ekler."""
    logging.raiseExceptions = False  # Handler hata atarsa Python'u susturma

    handler = PostgresLogHandler(level=logging.INFO)
    handler.setFormatter(logging.Formatter('%(message)s'))

    # app.logger'a ekle (Flask'ın kendi logger'ı)
    flask_app.logger.addHandler(handler)

    # Werkzeug ve diğer loggerlara da ekle ki tüm kanallardan yakalayalım
    for name in ('werkzeug', 'app', 'core', 'routes'):
        lg = logging.getLogger(name)
        lg.addHandler(handler)
        if lg.level == logging.NOTSET:
            lg.setLevel(logging.INFO)

    flask_app.logger.info("📝 PostgresLogHandler aktif — sistem logları app_log tablosuna yazılıyor")
