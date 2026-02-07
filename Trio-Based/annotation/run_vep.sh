#!/bin/bash

vep \
  -i input/trio.vcf.gz \
  -o annotation/trio.annotated.vcf.gz \
  --vcf \
  --cache \
  --assembly GRCh38 \
  --symbol \
  --hgvs \
  --canonical \
  --clin_sig \
  --af_gnomad \
  --everything \
  --fork 4
