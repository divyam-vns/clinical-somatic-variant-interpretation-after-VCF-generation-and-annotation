# Clinical Variant Interpretation Pipeline

This pipeline supports trio-based clinical interpretation of SNVs/indels
following variant calling. It integrates automated filtering with mandatory
human curation checkpoints per ACMG/AMP and CAP/CLIA standards.

Automation assists interpretation; final classification requires human review.

# Clinical Variant Interpretation Pipeline (Trio-Based)

**Purpose:**
From VCF + BAM + PED → ACMG-classified variants → clinical report inputs
**Audience:**
Variant Curation Scientists, Molecular Geneticists, Clinical Bioinformaticians

## WHERE HUMAN CURATION IS REQUIRED
| Step              | Automation | Human |
| ----------------- | ---------- | ----- |
| Annotation        | ✅          | ❌     |
| Inheritance       | ✅          | ❌     |
| BAM QC            | ❌          | ✅     |
| Phenotype match   | ❌          | ✅     |
| ACMG weighting    | ❌          | ✅     |
| Report narrative  | ❌          | ✅     |
| Clinical sign-out | ❌          | ✅     |

## Summary
This pipeline uses automation for annotation and inheritance filtering, but enforces human checkpoints at BAM review, ACMG classification, phenotype correlation, and report interpretation to meet CAP/CLIA requirements.
