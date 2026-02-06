# Annotation Databases

This directory contains scripts to download and prepare annotation databases
used for clinical somatic variant interpretation.

## Databases Included

| Database | Purpose | Source |
|--------|--------|--------|
| VEP Cache | Variant consequences | Ensembl |
| ClinVar | Clinical significance | NCBI |
| COSMIC | Somatic mutation hotspots | Sanger |

## Quick Start

```
bash download_all.sh
```

## COSMIC Notes

COSMIC requires authentication.
Download manually and place the VCF file in:
```
resources/dbs/cosmic/
```

Expected filename:
```
CosmicMutantExport_GRCh38_v97.vcf.gz
```

## Integration with VEP

Example VEP usage:
```
vep \
  --cache \
  --dir_cache resources/dbs/vep_cache \
  --plugin ClinVar,resources/dbs/clinvar/clinvar.vcf.gz \
  --plugin COSMIC,resources/dbs/cosmic/CosmicMutantExport_GRCh38_v97.vcf.gz
```

---

# Clinical-Grade Notes (Interview-Safe)

> “After VCF generation, variants are annotated using VEP with ClinVar and COSMIC. ClinVar supports AMP pathogenicity evidence, while COSMIC identifies somatic recurrence and hotspots critical for Tier I/II classification.”

---```
## VEP COMMAND WITH FULL CLINICAL FLAGS (Somatic-focused)
This assumes:
- GRCh38
- Local cache
- ClinVar + COSMIC
- Ready for AMP interpretation

```
 workflows/annotate_with_vep.sh
```
## in script - Why this matters clinically
| Flag             | Reason                                  |
| ---------------- | --------------------------------------- |
| `--everything`   | Covers consequence, protein, population |
| `ClinVar plugin` | AMP pathogenic evidence                 |
| `COSMIC plugin`  | Somatic recurrence                      |
| `pick_order`     | Transcript standardization              |
| `SpliceAI`       | BP7 / PP3                               |
| `CADD`           | Computational support                   |


## CIViC + OncoKB INTEGRATION (Post-VEP)

These are knowledgebase lookups, not VEP plugins.

## CIViC (Open, API-based)
``
scripts/query_civic.py
``

### Used for:

- AMP Tier I / II

- Drug–gene–variant relationships

- Predictive / therapeutic evidence

## OncoKB (Requires API Key)
```
scripts/query_oncokb.py
```

### Used for:
- FDA-approved therapy mapping
- NCCN relevance
- AMP Tier I/II decision

## 3. AMP TIER I–IV AUTO-CLASSIFICATION LOGIC
```
scripts/amp_classifier.py
```
| Evidence         | Source          |
| ---------------- | --------------- |
| Therapy approved | OncoKB          |
| Investigational  | CIViC           |
| Recurrence       | COSMIC          |
| Pathogenic       | ClinVar         |
| In silico        | CADD / SpliceAI |

## 4. FINAL CLINICAL JSON REPORT SCHEMA

This is exactly what labs expect.
```
resources/template/report_schema.json
```

## Explaination

“After VCF generation, variants are annotated using VEP with ClinVar, COSMIC, CADD, and SpliceAI. We then integrate CIViC and OncoKB for therapeutic and clinical evidence. Variants are automatically classified into AMP Tier I–IV using evidence-based rules, and results are delivered in a structured clinical JSON report.”

That answer alone clears bioinformatics + clinical interpretation screens.
