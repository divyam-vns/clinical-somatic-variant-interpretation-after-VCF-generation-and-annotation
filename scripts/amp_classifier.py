def classify_amp(row):
    """
    AMP/ASCO/CAP 2017
    """

    # Tier I: Strong Clinical Significance
    if row['oncokb_tx_level'] in ['1', '2'] or row['civic_evidence_level'] == 'A':
        return "Tier I"

    # Tier II: Potential Clinical Significance
    if row['oncokb_tx_level'] in ['3A', '3B'] or row['civic_evidence_level'] in ['B', 'C']:
        return "Tier II"

    # Tier III: Unknown Clinical Significance
    if row['cosmic_count'] > 1 or row['predicted_damaging']:
        return "Tier III"

    # Tier IV: Benign / Likely Benign
    return "Tier IV"
