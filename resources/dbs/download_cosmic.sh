#!/usr/bin/env bash
set -euo pipefail

COSMIC_DIR=$(pwd)/cosmic
ASSEMBLY=GRCh38
VERSION=v97

mkdir -p "$COSMIC_DIR"
cd "$COSMIC_DIR"

echo "COSMIC download requires authentication."
echo "Please download manually from:"
echo "https://cancer.sanger.ac.uk/cosmic/download"

echo "Expected file:"
echo "  CosmicMutantExport_${ASSEMBLY}_${VERSION}.vcf.gz"

if [[ ! -f CosmicMutantExport_${ASSEMBLY}_${VERSION}.vcf.gz ]]; then
  echo "ERROR: COSMIC VCF not found."
  exit 1
fi

echo "Indexing COSMIC VCF..."
tabix -p vcf CosmicMutantExport_${ASSEMBLY}_${VERSION}.vcf.gz

echo "COSMIC ready."
