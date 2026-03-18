from functools import wraps
from flask import session, request, redirect, url_for, jsonify
from core.config import ayar_getir
import logging
_log = logging.getLogger('app')

def ogretmen_giris_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('ogretmen'):
            # JSON API için 401 dön, sayfa için redirect
            if request.path.startswith('/api/'):
                return jsonify({'hata': 'Öğretmen girişi gerekli'}), 401
            # Blueprint isimleriyle uyumlu olması için redirect'i spesifik bir fonksiyona yönlendireceğiz.
            # Fakat view func ismi her projede genelde `teacher_bp.login` vs olur.
            return redirect(url_for('teacher_bp.ogretmen_giris'))
        return f(*args, **kwargs)
    return decorated

def seb_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        kiosk_modu = ayar_getir('kiosk_modu', '1') == '1'
        if kiosk_modu:
            user_agent = request.headers.get('User-Agent', '')
            # SEB tespiti: Windows "SEB/3.x", macOS "SafeExamBrowser"
            is_seb = 'SEB/' in user_agent or 'SafeExamBrowser' in user_agent
            _log.info(f"[SEB CHECK] path={request.path} is_seb={is_seb} UA={user_agent[:120]}")
            if not is_seb:
                return redirect(url_for('student_bp.seb_gerekli_sayfasi'))
        return f(*args, **kwargs)
    return decorated
