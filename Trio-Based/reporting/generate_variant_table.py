import pandas as pd

df = pd.DataFrame([{
    "Gene": "SCN2A",
    "Variant": "c.1234G>A (p.Arg412His)",
    "Inheritance": "De novo",
    "ACMG": "Likely Pathogenic",
    "Evidence": "PS2, PM2, PM1, PP3, PP4"
}])

df.to_csv("reporting/variant_table.csv", index=False)

# Variant Table for Report
