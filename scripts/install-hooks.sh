#!/usr/bin/env bash
# Git hooks kurulumu — scripts/git-hooks/ klasörünü aktif hooks dizini olarak ayarlar.
#
# Bu yaklaşım .git/hooks/ klasörünü değiştirmek yerine core.hooksPath config'i
# kullanır — hooks git'te versiyonlanır ve clone edildikten sonra tek komutla aktifleşir.
#
# Kullanım (proje clone edildikten sonra bir kez):
#   bash scripts/install-hooks.sh

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

HOOKS_DIR="scripts/git-hooks"

if [ ! -d "$HOOKS_DIR" ]; then
    echo "❌ $HOOKS_DIR bulunamadı."
    exit 1
fi

# Tüm hook dosyalarını executable yap
chmod +x "$HOOKS_DIR"/* 2>/dev/null || true

# Git'i bu dizini kullanmaya yönlendir
git config core.hooksPath "$HOOKS_DIR"

echo "✅ Git hooks aktif: $HOOKS_DIR"
echo ""
echo "Kurulu hook'lar:"
ls -1 "$HOOKS_DIR" | sed 's/^/  - /'
echo ""
echo "Devre dışı bırakmak için: git config --unset core.hooksPath"
