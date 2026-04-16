import pytest
from flask import session

def test_teacher_login_logout(client):
    """Öğretmen giriş ve çıkış akışını test eder."""
    # 1. Giriş sayfası kontrolü
    res = client.get('/teacher/login')
    assert res.status_code == 200
    assert "Giris" in res.data.decode('utf-8') or "Şifre" in res.data.decode('utf-8')

    # 2. Hatalı şifre denemesi
    res = client.post('/teacher/login', data={'sifre': 'yanlis_sifre'}, follow_redirects=True)
    assert "Hatalı şifre!" in res.data.decode('utf-8')

    # 3. Doğru şifre ile giriş (test_verilerini_yukle 1234 set ediyor)
    res = client.post('/teacher/login', data={'sifre': '1234'}, follow_redirects=True)
    assert res.status_code == 200
    assert "Panel" in res.data.decode('utf-8') or "Öğretmen" in res.data.decode('utf-8')
    
    with client.session_transaction() as sess:
        assert sess.get('ogretmen') is True

    # 4. Çıkış yapma
    res = client.get('/teacher/logout', follow_redirects=True)
    assert "Giris" in res.data.decode('utf-8') or "Şifre" in res.data.decode('utf-8')
    with client.session_transaction() as sess:
        assert sess.get('ogretmen') is None

def test_student_login_simple(client):
    """Öğrenci giriş akışını test eder."""
    # 1. Ana sayfa (Login) kontrolü
    res = client.get('/')
    assert res.status_code == 200
    assert "Giris" in res.data.decode('utf-8') or "Numara" in res.data.decode('utf-8')

    # 2. Öğrenci girişi (test1 öğrencisi)
    # routes/student.py: /giris -> sinif_id, ad_soyad, numara, ders_paketi
    # Önemli: Girişin açık olması lazım (test_verilerini_yukle ayarlar 'giris_acik' set etmiyor olabilir)
    # Ayarlardan girişi açalım (önce öğretmen girişi yapıp açabiliriz veya DB'ye manuel ekleyebiliriz)
    
    from core.config import ayar_kaydet, ders_durumu
    ayar_kaydet('giris_acik', '1')
    ders_durumu['giris_acik'] = True

    # test_verilerini_yukle() içinde 1 numaralı sınıf ID=1 olmalı
    data = {
        'sinif_id': '1',
        'ad_soyad': 'Öğrenci-1 TEST',
        'numara': 'test1',
        'ders_paketi': '1. Paket (09:00-11:35)'
    }
    res = client.post('/giris', data=data, follow_redirects=True)
    assert res.status_code == 200
    
    # Başarılı giriş sonrası ogrenci_ana.html yüklenmeli
    assert "bekleyiniz" in res.data.decode('utf-8') or "Ders Başladı" in res.data.decode('utf-8')
    
    with client.session_transaction() as sess:
        assert sess.get('numara') == 'test1'
