#!/usr/bin/env python3
"""
Yük Testi — 40 eşzamanlı öğrenci girişi simülasyonu

Kullanım:
    1. Sunucuyu test modunda başlat:  python app.py --test
    2. Başka terminalde:              python tests/yuk_testi.py

Seçenekler:
    --host HOST     Sunucu adresi (varsayılan: http://localhost:3333)
    --count N       Öğrenci sayısı (varsayılan: 40)
    --delay SECS    Her batch arası bekleme (varsayılan: 0)
    --batch N       Aynı anda kaç request (varsayılan: hepsi)
"""

import asyncio
import aiohttp
import time
import sys
import argparse
import json
from dataclasses import dataclass, field


@dataclass
class TestSonuc:
    numara: str
    basarili: bool
    sure_ms: float
    hata: str = ''
    status_code: int = 0


@dataclass
class RaporOzet:
    toplam: int = 0
    basarili: int = 0
    basarisiz: int = 0
    min_ms: float = 99999
    max_ms: float = 0
    ort_ms: float = 0
    hatalar: list = field(default_factory=list)
    sonuclar: list = field(default_factory=list)


async def ogrenci_giris(session: aiohttp.ClientSession, host: str, numara: str, sinif_id: int = 99) -> TestSonuc:
    """Tek öğrenci giriş simülasyonu."""
    ad_soyad = f'TEST{numara[1:].lstrip("0") or "0"} OGRENCI'
    if numara[1:].lstrip("0"):
        ad_soyad = f'TEST{int(numara[1:]):02d} OGRENCI'

    form_data = {
        'sinif_id': str(sinif_id),
        'ad_soyad': ad_soyad.upper(),
        'numara': numara,
        'ders_paketi': '1. Paket (09:00-11:35)'
    }

    baslangic = time.monotonic()
    try:
        async with session.post(
            f'{host}/giris',
            data=form_data,
            allow_redirects=False,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            sure = (time.monotonic() - baslangic) * 1000

            # Başarılı giriş = 302 redirect veya 200
            if resp.status in (302, 303, 200):
                return TestSonuc(numara=numara, basarili=True, sure_ms=sure, status_code=resp.status)
            else:
                body = await resp.text()
                hata_mesaj = ''
                if 'hata' in body.lower():
                    # HTML'den hata mesajını çıkar
                    import re
                    match = re.search(r'⚠️\s*(.+?)</div>', body)
                    if match:
                        hata_mesaj = match.group(1).strip()
                return TestSonuc(numara=numara, basarili=False, sure_ms=sure, hata=hata_mesaj or f'HTTP {resp.status}', status_code=resp.status)

    except asyncio.TimeoutError:
        sure = (time.monotonic() - baslangic) * 1000
        return TestSonuc(numara=numara, basarili=False, sure_ms=sure, hata='TIMEOUT (30s)')
    except Exception as e:
        sure = (time.monotonic() - baslangic) * 1000
        return TestSonuc(numara=numara, basarili=False, sure_ms=sure, hata=str(e))


async def api_durum_kontrol(session: aiohttp.ClientSession, host: str) -> dict:
    """Sunucu durumunu kontrol et."""
    try:
        async with session.get(f'{host}/api/yoklama', timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                return await resp.json()
            return {'hata': f'HTTP {resp.status}'}
    except Exception as e:
        return {'hata': str(e)}


async def calistir(host: str, count: int, batch_size: int, delay: float):
    """Ana test fonksiyonu."""
    print('\n' + '=' * 60)
    print('  🧪 Yük Testi — Eşzamanlı Öğrenci Giriş Simülasyonu')
    print('=' * 60)
    print(f'  Hedef:     {host}')
    print(f'  Öğrenci:   {count}')
    print(f'  Batch:     {batch_size}')
    print(f'  Delay:     {delay}s')
    print('=' * 60 + '\n')

    rapor = RaporOzet()

    # Bağlantı havuzu
    connector = aiohttp.TCPConnector(limit=count, limit_per_host=count)

    async with aiohttp.ClientSession(connector=connector) as session:
        # Sunucu erişilebilir mi?
        print('  📡 Sunucu kontrol ediliyor...')
        try:
            async with session.get(f'{host}/', timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status not in (200, 302):
                    print(f'  ❌ Sunucu yanıt vermiyor (HTTP {resp.status})')
                    return
            print('  ✅ Sunucu erişilebilir\n')
        except Exception as e:
            print(f'  ❌ Sunucu erişilemiyor: {e}')
            print(f'     Sunucuyu "python app.py --test" ile başlattığından emin ol.')
            return

        # Öğrenci numaralarını oluştur
        numaralar = [f'T{i:04d}' for i in range(1, count + 1)]

        # Batch halinde gönder
        tum_baslangic = time.monotonic()
        tum_sonuclar = []

        for batch_start in range(0, len(numaralar), batch_size):
            batch = numaralar[batch_start:batch_start + batch_size]
            batch_no = (batch_start // batch_size) + 1
            toplam_batch = (len(numaralar) + batch_size - 1) // batch_size

            print(f'  🚀 Batch {batch_no}/{toplam_batch} — {len(batch)} öğrenci gönderiliyor...')

            tasks = [ogrenci_giris(session, host, numara) for numara in batch]
            sonuclar = await asyncio.gather(*tasks, return_exceptions=True)

            for s in sonuclar:
                if isinstance(s, Exception):
                    tum_sonuclar.append(TestSonuc(numara='?', basarili=False, sure_ms=0, hata=str(s)))
                else:
                    tum_sonuclar.append(s)

            # Batch sonucu
            basarili = sum(1 for s in sonuclar if not isinstance(s, Exception) and s.basarili)
            print(f'     ✅ {basarili}/{len(batch)} başarılı')

            if delay > 0 and batch_start + batch_size < len(numaralar):
                await asyncio.sleep(delay)

        toplam_sure = (time.monotonic() - tum_baslangic) * 1000

        # Rapor oluştur
        rapor.toplam = len(tum_sonuclar)
        rapor.sonuclar = tum_sonuclar

        sureler = []
        for s in tum_sonuclar:
            if s.basarili:
                rapor.basarili += 1
                sureler.append(s.sure_ms)
            else:
                rapor.basarisiz += 1
                rapor.hatalar.append(f'{s.numara}: {s.hata}')

        if sureler:
            rapor.min_ms = min(sureler)
            rapor.max_ms = max(sureler)
            rapor.ort_ms = sum(sureler) / len(sureler)

        # Rapor yazdır
        print('\n' + '=' * 60)
        print('  📊 Test Raporu')
        print('=' * 60)
        print(f'  Toplam:       {rapor.toplam}')
        print(f'  Başarılı:     {rapor.basarili} ({rapor.basarili/rapor.toplam*100:.0f}%)' if rapor.toplam > 0 else '')
        print(f'  Başarısız:    {rapor.basarisiz}')
        print(f'  Toplam Süre:  {toplam_sure:.0f}ms ({toplam_sure/1000:.1f}s)')
        if sureler:
            print(f'  Min Yanıt:    {rapor.min_ms:.0f}ms')
            print(f'  Max Yanıt:    {rapor.max_ms:.0f}ms')
            print(f'  Ort Yanıt:    {rapor.ort_ms:.0f}ms')

            # Percentiles
            sureler.sort()
            p50 = sureler[len(sureler) // 2]
            p95 = sureler[int(len(sureler) * 0.95)]
            p99 = sureler[int(len(sureler) * 0.99)]
            print(f'  P50:          {p50:.0f}ms')
            print(f'  P95:          {p95:.0f}ms')
            print(f'  P99:          {p99:.0f}ms')

        if rapor.hatalar:
            print(f'\n  ⚠️ Hatalar ({len(rapor.hatalar)}):')
            for h in rapor.hatalar[:10]:
                print(f'    - {h}')
            if len(rapor.hatalar) > 10:
                print(f'    ... ve {len(rapor.hatalar) - 10} hata daha')

        # Yoklama kontrolü
        print('\n  📋 Yoklama Kontrolü...')
        durum = await api_durum_kontrol(session, host)
        if 'ogrenciler' in durum:
            print(f'     Yoklama kaydı: {len(durum["ogrenciler"])} öğrenci')
        elif 'hata' in durum:
            print(f'     ⚠️ Yoklama kontrolü başarısız: {durum["hata"]}')

        print('=' * 60)

        # Sonuç değerlendirme
        if rapor.basarili == rapor.toplam:
            print('  ✅ TÜM TESTLER BAŞARILI!')
        elif rapor.basarili > rapor.toplam * 0.9:
            print(f'  ⚠️ %{rapor.basarili/rapor.toplam*100:.0f} başarı — kabul edilebilir')
        else:
            print(f'  ❌ %{rapor.basarili/rapor.toplam*100:.0f} başarı — sorun var!')
        print('=' * 60 + '\n')


def main():
    parser = argparse.ArgumentParser(description='Ders Takip Yük Testi')
    parser.add_argument('--host', default='http://localhost:3333', help='Sunucu adresi')
    parser.add_argument('--count', type=int, default=40, help='Öğrenci sayısı')
    parser.add_argument('--batch', type=int, default=0, help='Batch boyutu (0=hepsi)')
    parser.add_argument('--delay', type=float, default=0, help='Batch arası bekleme (saniye)')
    args = parser.parse_args()

    if args.batch <= 0:
        args.batch = args.count

    asyncio.run(calistir(args.host, args.count, args.batch, args.delay))


if __name__ == '__main__':
    main()
