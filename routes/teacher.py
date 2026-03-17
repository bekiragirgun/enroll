from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from core.security import ogretmen_giris_gerekli
from core.utils import bugun, slayt_listesi
from core.config import ders_durumu, ayar_getir, ayar_kaydet

VARSAYILAN_SIFRE = 'linux2024'
teacher_bp = Blueprint('teacher_bp', __name__, url_prefix='/teacher')

def _ogretmen_sifre():
    return ayar_getir('ogretmen_sifre', VARSAYILAN_SIFRE)

@teacher_bp.route('/login', methods=['GET', 'POST'])
def ogretmen_giris():
    hata = None
    if request.method == 'POST':
        if request.form.get('sifre') == _ogretmen_sifre():
            session['ogretmen'] = True
            return redirect(url_for('teacher_bp.ogretmen_panel'), 303)
        hata = 'Hatalı şifre!'
    return render_template('ogretmen_giris.html', hata=hata)

@teacher_bp.route('/logout')
def ogretmen_cikis():
    session.pop('ogretmen', None)
    return redirect(url_for('teacher_bp.ogretmen_giris'))

@teacher_bp.route('/')
@ogretmen_giris_gerekli
def ogretmen_panel():
    return render_template(
        'ogretmen.html',
        tarih=bugun(),
        slaytlar=slayt_listesi(),
        aktif_mod=ders_durumu['mod'],
        aktif_dosya=ders_durumu['dosya'],
        config=ders_durumu
    )

@teacher_bp.route('/sifre_degistir', methods=['POST'])
@ogretmen_giris_gerekli
def ogretmen_sifre_degistir():
    veri = request.get_json()
    mevcut = veri.get('mevcut', '')
    yeni = veri.get('yeni', '')
    if not mevcut or not yeni:
        return jsonify({'durum': 'hata', 'mesaj': 'Mevcut ve yeni şifre gerekli'}), 400
    if mevcut != _ogretmen_sifre():
        return jsonify({'durum': 'hata', 'mesaj': 'Mevcut şifre hatalı'}), 403
    if len(yeni) < 4:
        return jsonify({'durum': 'hata', 'mesaj': 'Yeni şifre en az 4 karakter olmalı'}), 400
    ayar_kaydet('ogretmen_sifre', yeni)
    return jsonify({'durum': 'ok', 'mesaj': 'Şifre başarıyla değiştirildi'})

@teacher_bp.route('/terminal')
@ogretmen_giris_gerekli
def ogretmen_terminal_sayfasi():
    """Öğretmen terminal yayın sayfası."""
    return render_template('ogretmen_terminal.html')
