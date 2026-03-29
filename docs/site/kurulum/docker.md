# Docker Compose Kurulumu

Production ortami Docker Compose ile calisir: PostgreSQL + Flask.

## Baslat

```bash
docker compose up -d
```

## Durdur

```bash
docker compose down
```

## Servisler

| Servis | Image | Port | Aciklama |
|--------|-------|------|----------|
| `db` | postgres:15 | 5432 | PostgreSQL veritabani |
| `app` | python:3.11-slim | 3333 | Flask + SocketIO |

## Ortam Degiskenleri (`.env`)

```env
DB_TYPE=postgres
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres_pass
DB_NAME=ders_takip
SECRET_KEY=your-secret-key
```

## Veri Kaliciligi

PostgreSQL verileri `./postgres_data/` dizininde saklanir (volume mount).

!!! danger "Dikkat"
    `postgres_data/` dizinini silmeyin — tum yoklama, ogrenci ve sinav verileri burada.
    `.gitignore`'da oldugu icin git'e commit edilmez.

## Loglar

```bash
# Tum loglar
docker compose logs -f

# Sadece uygulama
docker compose logs -f app

# Sadece veritabani
docker compose logs -f db
```

## Yeniden Olusturma

```bash
docker compose up --build -d
```
