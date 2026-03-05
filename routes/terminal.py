from flask import Blueprint, render_template, request, redirect, session, current_app
from core.db import db_baglantisi
from core.utils import bugun, simdi, istemci_ip
import logging

log = logging.getLogger('app')
terminal_bp = Blueprint('terminal_bp', __name__, url_prefix='/terminal')

@terminal_bp.route('/', strict_slashes=False)
def terminal_sayfasi():
    """Terminal doğrulama ve otomatik yönlendirme sayfası."""
    if not session.get('numara'):
        return render_template('terminal_login.html', hata='Önce ana sayfadan giriş yapmalısınız.')

    session_numara = session['numara']
    session_ad = session.get('ad', '')
    session_soyad = session.get('soyad', '')

    if session.get('terminal_numara') != session_numara:
        from chroot_terminal import chroot_var_mi, chroot_olustur, chroot_ip_al
        if not chroot_var_mi(session_numara):
            log.info(f"Otomatik terminal girişi için chroot oluşturuluyor: {session_numara}")
            chroot_olustur(session_numara, session_ad, session_soyad)
            
        ssh_ip = chroot_ip_al(session_numara)
        session['terminal_numara'] = session_numara
        session['terminal_ad'] = session_ad
        session['terminal_soyad'] = session_soyad
        session['terminal_ip'] = ssh_ip
        
        try:
            with db_baglantisi() as db:
                db.execute("""
                    INSERT INTO terminal_guvenlik_log
                    (tarih, saat, ip, session_numara, session_ad, girilen_numara, durum)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (bugun(), simdi(), istemci_ip(), session_numara, f"{session_ad} {session_soyad}".strip(), session_numara, 'OTOMATIK_GIRIS'))
                db.commit()
        except: pass

    return redirect('/terminal/workspace')

@terminal_bp.route('/login', methods=['POST'])
def terminal_login():
    """Terminal login ve güvenlik kontrolü."""
    session_numara = session.get('numara', '')
    session_ad = session.get('ad', '')
    session_soyad = session.get('soyad', '')
    session_ad_soyad = f"{session_ad} {session_soyad}".strip()
    girilen_numara = request.form.get('numara_dogrulama', '').strip()

    if not girilen_numara or not girilen_numara.isdigit():
        return render_template('terminal_guvenlik.html', session_numara=session_numara, session_ad=session_ad, session_soyad=session_soyad, session_ad_soyad=session_ad_soyad, hata='Geçerli bir numara girin.')

    ip = istemci_ip()
    if girilen_numara == session_numara:
        with db_baglantisi() as db:
            db.execute("INSERT INTO terminal_guvenlik_log (tarih, saat, ip, session_numara, session_ad, girilen_numara, durum) VALUES (?, ?, ?, ?, ?, ?, ?)", (bugun(), simdi(), ip, session_numara, session_ad_soyad, girilen_numara, 'BASARILI'))
            db.commit()

        from chroot_terminal import chroot_var_mi, chroot_olustur, chroot_ip_al
        if not chroot_var_mi(girilen_numara):
            chroot_olustur(girilen_numara, session_ad, session_soyad)

        ssh_ip = chroot_ip_al(girilen_numara)
        session['terminal_numara'] = girilen_numara
        session['terminal_ad'] = session_ad
        session['terminal_soyad'] = session_soyad
        session['terminal_ip'] = ssh_ip
        return redirect('/terminal/workspace')
    else:
        with db_baglantisi() as db:
            db.execute("INSERT INTO terminal_guvenlik_log (tarih, saat, ip, session_numara, session_ad, girilen_numara, durum) VALUES (?, ?, ?, ?, ?, ?, ?)", (bugun(), simdi(), ip, session_numara, session_ad_soyad, girilen_numara, 'GUVENLIK_IHLALI'))
            db.commit()
        # To avoid circular import, importing socketio dynamically here if needed or handled elsewhere 
        # But emit can be called from imported module if properly structured
        try:
            from app import socketio
            mesaj = (
                f"⚠️ GÜVENLİK UYARISI ⚠️\n\nTerminal Erişim İhlali!\n\n"
                f"Oturum açan: {session_ad_soyad} ({session_numara})\n"
                f"Girmeye çalışan: {girilen_numara}\nIP: {ip}\nTarih: {bugun()} {simdi()}"
            )
            socketio.emit('guvenlik_uyari', mesaj, namespace='/terminal')
        except: pass

        return render_template('terminal_guvenlik.html', session_numara=session_numara, session_ad=session_ad, session_soyad=session_soyad, session_ad_soyad=session_ad_soyad, hata=(f"⚠️ GÜVENLİK UYARISI!\n\nBu terminal {session_numara} numaralı öğrenci içindir.\nSiz {girilen_numara} numarasını girdiniz.\n\nBu erişim girişimi LOGlanmıştır ve öğretmene bildirilmiştir."))

@terminal_bp.route('/workspace')
def terminal_workspace():
    """Terminal çalışma alanı - authentication gerekli."""
    if not session.get('terminal_numara'):
        return redirect('/terminal')

    numara = session['terminal_numara']
    ad = session['terminal_ad']
    soyad = session['terminal_soyad']
    ip = session['terminal_ip']

    return render_template('terminal_workspace.html', numara=numara, ad_soyad=f"{ad} {soyad}".upper(), container_ip=ip)
