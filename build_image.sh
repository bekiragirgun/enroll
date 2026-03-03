#!/bin/bash
set -e
echo "🐳 Öğrenci terminal imajı oluşturuluyor..."
docker build -t ogrenci-terminal:latest .
echo "✅ İmaj hazır: ogrenci-terminal:latest"
docker images | grep ogrenci-terminal
