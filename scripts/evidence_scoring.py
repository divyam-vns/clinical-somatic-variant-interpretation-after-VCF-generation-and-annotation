import yaml
import pandas as pd

def score_variant(row, rules):
    score = 0
    ev = []
    for crit, cfg in rules.items():
        if crit == "PopulationFreq":
            if row['AF'] < cfg['threshold']:
                score += cfg['weight']; ev.append(crit)
        elif crit == "ClinVarPathogenic":
            if "Pathogenic" in row['clin_sign']:
                score += cfg['weight']; ev.append(crit)
    return score, ev

# CLI Handling omitted for brevity
