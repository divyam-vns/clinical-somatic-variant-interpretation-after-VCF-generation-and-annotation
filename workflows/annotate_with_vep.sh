#!/usr/bin/env bash
set -euo pipefail

VCF_IN=$1
VCF_OUT=$2

VEP_CACHE=resources/dbs/vep_cache
PLUGIN_DIR=resources/dbs/vep_plugins
CLINVAR=resources/dbs/clinvar/clinvar.vcf.gz
COSMIC=resources/dbs/cosmic/CosmicMutantExport_GRCh38_v97.vcf.gz

vep \
  --input_file "$VCF_IN" \
  --output_file "$VCF_OUT" \
  --vcf \
  --cache \
  --offline \
  --dir_cache "$VEP_CACHE" \
  --assembly GRCh38 \
  --species homo_sapiens \
  --everything \
  --fork 8 \
  --no_stats \
  --compress_output bgzip \
  \
  --plugin ClinVar,"$CLINVAR" \
  --plugin COSMIC,"$COSMIC" \
  --plugin CADD,"$PLUGIN_DIR/whole_genome_SNVs.tsv.gz" \
  --plugin SpliceAI,snv="$PLUGIN_DIR/spliceai_scores.raw.snv.hg38.vcf.gz" \
  \
  --flag_pick \
  --pick_order canonical,appris,tsl,biotype,ccds,rank \
  \
  --custom "$CLINVAR",ClinVar,vcf,exact,0,CLNSIG,CLNREVSTAT \
  --custom "$COSMIC",COSMIC,vcf,exact,0,COSMIC_ID,CNT
