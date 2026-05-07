#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
python -m pip install pyinstaller==6.11.1
pyinstaller --noconfirm ArchitectureNoticeLauncher.spec

echo "빌드 완료: dist/ArchitectureNoticeLauncher"
