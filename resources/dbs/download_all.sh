#!/usr/bin/env bash
set -euo pipefail

echo "Starting full annotation DB setup..."

bash download_vep.sh
bash download_clinvar.sh
bash download_cosmic.sh || true

echo "Database setup completed."
