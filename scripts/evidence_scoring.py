
import argparse
import yaml
import pandas as pd

def classify_tier(score):

    if score >= 10:
        return "Tier I"

    elif score >= 6:
        return "Tier II"

    elif score >= 3:
        return "Tier III"

    return "Tier IV"

def score_variant(row, rules, cancer_type):

    score = 0
    evidence = []

    effects = str(row["effects"])
    clin = str(row["clin_sign"])

    if "Pathogenic" in clin:
        score += rules["ClinVarPathogenic"]["weight"]
        evidence.append("ClinVarPathogenic")

    for key, cfg in rules.items():

        if isinstance(cfg, dict) and "gene" in cfg:

            gene = cfg["gene"]

            if gene in effects:

                if (
                    cfg["cancer"] == cancer_type
                    or cfg["cancer"] == "any"
                ):

                    score += cfg["weight"]
                    evidence.append(key)

    return score, evidence

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--table", required=True)
    parser.add_argument("--cancer-type", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)

    args = parser.parse_args()

    df = pd.read_csv(args.table, sep="\t")

    with open(args.rules) as f:
        rules = yaml.safe_load(f)

    scores = []
    evidences = []
    tiers = []

    for _, row in df.iterrows():

        score, ev = score_variant(
            row,
            rules,
            args.cancer_type
        )

        tier = classify_tier(score)

        scores.append(score)
        evidences.append(";".join(ev))
        tiers.append(tier)

    df["score"] = scores
    df["evidence"] = evidences
    df["tier"] = tiers

    df.to_csv(args.out, sep="\t", index=False)

if __name__ == "__main__":
    main()
