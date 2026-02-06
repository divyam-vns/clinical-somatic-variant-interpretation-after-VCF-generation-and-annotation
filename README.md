# Clinical Somatic Variant Interpretation Pipeline

Automated somatic variant interpretation workflow that ingests **annotated VCF files**, applies **clinical evidence rules (AMP/ASCO/CAP)**, scores each variant, and outputs a **tiered JSON/TSV report**.

This workflow is loosely inspired by **Arti: Clinical Somatic Variant Annotation & Interpretation Tool**. :contentReference[oaicite:1]{index=1}

## Overview

1. **Input:** Pre-annotated VCF (e.g., VEP, ANNOVAR)
2. **Parsing:** Transform annotated fields to structured table
3. **Evidence Scoring:** Evaluate each variant against AMP criteria
4. **Classification:** Assign somatic tiers (I, II, III, IV)
5. **Output:** JSON + TSV clinical variant reports

## Requirements

- Docker (or Singularity)
- Nextflow
- Python 3.10+
- Python packages from `requirements.txt`

## Quickstart (CLI)

```bash
./scripts/run_interpretation.sh \
  --vcf example_data/sample1.vep.vcf.gz \
  --cancer-type lung \
  --output results/sample1_report.json
```
## AMP Clinical Rules
Clinical rules (AMP 4-tier system) are encoded in:
```
resources/amp_guidelines.yaml
```
You can customize scoring weights and rules.

## Tests
```
pytest tests/
```
```

---
# Core Scripts (Snippets)
### scripts/run_interpretation.sh

```bash
#!/bin/bash
set -euo pipefail

VCF=$1
CANCER_TYPE=$2
OUT=$3

python scripts/parse_vep_to_table.py \
  --input $VCF \
  --output tmp/variants_table.tsv

python scripts/evidence_scoring.py \
  --table tmp/variants_table.tsv \
  --cancer-type $CANCER_TYPE \
  --rules resources/amp_guidelines.yaml \
  --out scored_variants.tsv

python scripts/generate_report.py \
  --scored scored_variants.tsv \
  --template resources/template/report_template.json \
  --out $OUT
