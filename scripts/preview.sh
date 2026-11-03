#!/usr/bin/env bash
# Build and serve RunicDocs locally with Quartz (needs Node 22+ and git).
# First run downloads Quartz into .quartz/ (ignored by git); later runs reuse it.
# Open http://localhost:8080 when the build finishes. Re-run after editing notes.
set -euo pipefail

QUARTZ_VERSION="${QUARTZ_VERSION:-v5.0.0}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -d .quartz ]; then
  git clone --depth 1 --branch "$QUARTZ_VERSION" https://github.com/jackyzha0/quartz.git .quartz
  (cd .quartz && npm ci && npx quartz plugin restore)
fi

rm -rf .quartz/content
cp -r content .quartz/content
cp quartz.config.yaml .quartz/quartz.config.yaml

cd .quartz
npx quartz build --serve
