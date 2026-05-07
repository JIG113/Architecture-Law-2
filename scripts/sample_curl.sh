#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://127.0.0.1:8000}

curl -X POST "$BASE_URL/api/documents/upload" \
  -F "source_type=공고" \
  -F "issuing_org=OO도시공사" \
  -F "file=@README.md"
