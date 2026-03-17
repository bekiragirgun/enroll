import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# --test flag ile başlatılınca test DB kullanılır
TEST_MODE = os.environ.get('DERS_TAKIP_TEST', '0') == '1'
if TEST_MODE:
    DB_YOLU = BASE_DIR / 'data' / 'test_yoklama.db'
else:
    DB_YOLU = BASE_DIR / 'data' / 'yoklama.db'

SLAYT_DIR = BASE_DIR / 'slaytlar'
GORSELLER_DIR = BASE_DIR.parent / '01_SUNUMLAR' / 'gorseller'
