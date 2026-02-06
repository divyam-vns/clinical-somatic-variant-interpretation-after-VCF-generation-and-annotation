import requests

def query_civic(gene, variant):
    url = "https://civicdb.org/api/variants"
    params = {"gene": gene, "name": variant}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        "civic_evidence_level": data.get("evidence_level"),
        "civic_clinical_significance": data.get("clinical_significance"),
        "civic_drug": data.get("drugs")
    }
