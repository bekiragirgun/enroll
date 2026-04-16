import os
import sys
import pytest
import eventlet

# Monkey patch must be the very first thing for eventlet-based apps
eventlet.monkey_patch()

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment variables BEFORE importing app or core modules
os.environ['PATH'] = f"/opt/homebrew/bin:/usr/local/bin:{os.environ.get('PATH', '')}"
os.environ['DERS_TAKIP_TEST'] = '1'
os.environ['TEST_MODE'] = '1'
os.environ['DB_TYPE'] = 'sqlite'
# SSH ayarları artık doğrudan .env dosyasından okunacak
from app import app as flask_app, socketio
from core.db import db_olustur, test_verilerini_yukle
from core.paths import DB_YOLU

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    """Her test oturumu başında veritabanını sıfırdan oluşturur."""
    print(f"\n[Test] Veritabanı sıfırlanıyor: {DB_YOLU}")
    if DB_YOLU.exists():
        try:
            os.remove(DB_YOLU)
        except OSError:
            pass
            
    # Tabloları oluştur ve örnek verileri yükle
    db_olustur()
    test_verilerini_yukle(count=5) # 5 test öğrencisi yeterli
    
    yield
    
    # Oturum bittiğinde isterseniz silebilirsiniz, 
    # ancak incelemek için bırakmak bazen iyidir.
    # if DB_YOLU.exists(): os.remove(DB_YOLU)

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False, # Testler kolaylığı için CSRF'i kapattık
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def socket_client(app, client):
    return socketio.test_client(app, namespace='/terminal', flask_test_client=client)
