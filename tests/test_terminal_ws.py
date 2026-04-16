import pytest
import time
from unittest.mock import patch

def test_terminal_namespace_connection(socket_client):
    """Terminal namespace bağlantısını doğrular."""
    assert socket_client.is_connected(namespace='/terminal')

@patch('chroot_terminal.chroot_olustur')
def test_ogrenci_baglan_event(mock_olustur, app, client):
    """Öğrenci terminal bağlantı isteğini test eder (Mock SSH)."""
    mock_olustur.return_value = True

    # 1. Önce Session simülasyonu yap (Handshake öncesi çerezler hazır olmalı)
    with client.session_transaction() as sess:
        sess['numara'] = 'test1'
        sess['ad_soyad'] = 'Test Ogrenci'
        sess['sinif_id'] = '1'
        sess['ders_paketi'] = '1. Paket'

    # 2. Şimdi SocketIO client'ını oluştur (client'ın cookies'lerini otomatik alacak)
    from app import socketio
    socket_client = socketio.test_client(app, namespace='/terminal', flask_test_client=client)
    
    # 3. SocketIO üzerinden bağlan
    socket_client.emit('ogrenci_baglan', {'username': 'test1', 'sid': 'test-sid'}, namespace='/terminal')
    
    # Yanıtları kontrol et
    # Not: chroot_olustur ve SSH bağlantısı threading ile yapıldığı için 
    # 'container_hazir' biraz gecikebilir. Test client'ı bekletmek gerekebilir.
    
    timeout = 10  # 10 saniye limit
    start = time.time()
    container_hazir = False
    
    while time.time() - start < timeout:
        received = socket_client.get_received(namespace='/terminal')
        for msg in received:
            if msg['name'] == 'container_hazir':
                container_hazir = True
                break
        if container_hazir: break
        time.sleep(1.0)

    # Eğer 10.211.55.27 erişilebilir ise container_hazir gelmeli
    # Değilse 'hata' mesajı gelmeli. Her iki durumda da bir yanıt bekliyoruz.
    if not container_hazir:
        # Hata mesajı var mı bak
        received = socket_client.get_received(namespace='/terminal')
        for msg in received:
            if msg['name'] == 'hata':
                break
    
    # Biz en azından event'in işlendiğini doğrulamak istiyoruz.
    # Gerçek SSH bağlantısı başarılı olursa bu True dönecektir.
    assert container_hazir, "Terminal bağlantısı (container_hazir) gerçekleşmedi."

@patch('subprocess.Popen')
@patch('chroot_terminal.chroot_olustur')
def test_ogretmen_baglan_event(mock_olustur, mock_popen, app, client):
    """Öğretmen terminal bağlantı isteğini test eder (Mock SSH)."""
    mock_olustur.return_value = True
    # 1. Önce Session simülasyonu yap
    with client.session_transaction() as sess:
        sess['ogretmen'] = True
        sess['ogretmen_numara'] = 'root'

    # 2. Şimdi SocketIO client'ını oluştur
    from app import socketio
    socket_client = socketio.test_client(app, namespace='/terminal', flask_test_client=client)
    
    # 3. SocketIO üzerinden bağlan
    socket_client.emit('ogretmen_baglan', namespace='/terminal')
    
    timeout = 10
    start = time.time()
    received_any = False
    
    while time.time() - start < timeout:
        received = socket_client.get_received(namespace='/terminal')
        if received:
            received_any = True
            for msg in received:
                if msg['name'] == 'ogretmen_cikti':
                    return
        time.sleep(1)
    
    assert received_any, "Öğretmen terminalinden hiç yanıt alınamadı."
