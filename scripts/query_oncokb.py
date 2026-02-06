import requests
import os

API_KEY = os.environ.get("ONCOKB_API_KEY")

def query_oncokb(gene, alteration):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = "https://www.oncokb.org/api/v1/annotate/mutations/byProteinChange"
    params = {
        "hugoSymbol": gene,
        "alteration": alteration
    }
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        return None
    d = r.json()
    return {
        "oncokb_level": d.get("oncogenic"),
        "oncokb_tx_level": d.get("highestSensitiveLevel"),
        "oncokb_drug": d.get("drugs")
    }
