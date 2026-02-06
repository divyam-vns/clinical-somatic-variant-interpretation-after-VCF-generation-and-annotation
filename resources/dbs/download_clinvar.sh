#!/usr/bin/env bash
set -euo pipefail

CLINVAR_DIR=$(pwd)/clinvar
ASSEMBLY=GRCh38
RELEASE=latest

mkdir -p "$CLINVAR_DIR"
cd "$CLINVAR_DIR"

echo "Downloading ClinVar VCF..."

wget -O clinvar.vcf.gz \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_${ASSEMBLY}/clinvar.vcf.gz

wget -O clinvar.vcf.gz.tbi \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_${ASSEMBLY}/clinvar.vcf.gz.tbi

echo "ClinVar downloaded and indexed."
