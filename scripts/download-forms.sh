#!/usr/bin/env bash
# Download IRS form PDFs for a given tax year into forms/<year>/
# Usage: ./scripts/download-forms.sh [year]
# Default year: 2025

set -euo pipefail

YEAR="${1:-2025}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$SCRIPT_DIR/../forms/$YEAR"
BASE_URL="https://www.irs.gov/pub/irs-pdf"

mkdir -p "$DEST"

# Pairs of: local-filename irs-filename
FORMS=(
  "f1040.pdf"                f1040.pdf
  "f1040-schedule-1.pdf"     f1040s1.pdf
  "f1040-schedule-2.pdf"     f1040s2.pdf
  "f1040-schedule-3.pdf"     f1040s3.pdf
  "f1040-schedule-a.pdf"     f1040sa.pdf
  "f1040-schedule-b.pdf"     f1040sb.pdf
  "f1040-schedule-d.pdf"     f1040sd.pdf
  "f8949.pdf"                f8949.pdf
  "f8889.pdf"                f8889.pdf
  "f8995.pdf"                f8995.pdf
  "f1116.pdf"                f1116.pdf
  "f8812.pdf"                f8812.pdf
)

echo "Downloading IRS forms for tax year $YEAR into $DEST/"
echo ""

PASS=0
FAIL=0

i=0
while [[ $i -lt ${#FORMS[@]} ]]; do
  LOCAL="${FORMS[$i]}"
  IRS="${FORMS[$((i + 1))]}"
  URL="$BASE_URL/$IRS"
  OUT="$DEST/$LOCAL"

  printf "  %-40s" "$LOCAL"
  HTTP=$(curl -s -o "$OUT" -w "%{http_code}" "$URL")
  if [[ "$HTTP" == "200" ]]; then
    SIZE=$(du -h "$OUT" | cut -f1)
    echo "OK ($SIZE)"
    PASS=$((PASS + 1))
  else
    echo "FAILED (HTTP $HTTP)"
    rm -f "$OUT"
    FAIL=$((FAIL + 1))
  fi

  i=$((i + 2))
done

echo ""
echo "Done: $PASS downloaded, $FAIL failed."

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
