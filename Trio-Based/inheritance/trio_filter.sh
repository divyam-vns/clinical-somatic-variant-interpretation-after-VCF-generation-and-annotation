#!/bin/bash

bcftools view \
  -i 'GT[0]="het" && GT[1]="homref" && GT[2]="homref"' \
  annotation/trio.annotated.vcf.gz \
  > inheritance/denovo.vcf

bcftools view \
  -i 'GT[0]="hom" && GT[1]="het" && GT[2]="het"' \
  annotation/trio.annotated.vcf.gz \
  > inheritance/recessive.vcf
# Produces candidate variants only
