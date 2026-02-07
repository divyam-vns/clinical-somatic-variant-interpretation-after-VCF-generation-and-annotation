acmg = {
    "PS2": False,
    "PM2": False,
    "PM1": False,
    "PP3": False,
    "PP4": False
}

# Example logic
if denovo_confirmed:
    acmg["PS2"] = True

if gnomad_af == 0:
    acmg["PM2"] = True

if in_critical_domain:
    acmg["PM1"] = True

if cadd > 20:
    acmg["PP3"] = True

if phenotype_match:
    acmg["PP4"] = True

print(acmg)

# Human must confirm each criterion
