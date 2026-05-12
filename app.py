
import streamlit as st
import pandas as pd
import subprocess
from pathlib import Path
import sys

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="Clinical Somatic Variant Interpreter",
    layout="wide"
)

st.title("🧬 Clinical Somatic Variant Interpretation Pipeline")

st.markdown("""
AMP/ASCO/CAP-inspired somatic variant interpretation system.

Features:
- VCF parsing (VEP/ANN style)
- Evidence-based scoring
- Clinical tier classification
- Downloadable reports
""")

# ----------------------------
# Paths (CRITICAL FIX for Streamlit Cloud)
# ----------------------------
BASE_DIR = Path(__file__).parent

INPUT_VCF = BASE_DIR / "example_data" / "demo.vep.vcf"
RULES_FILE = BASE_DIR / "resources" / "amp_guidelines.yaml"
TMP_DIR = BASE_DIR / "tmp"

TMP_DIR.mkdir(exist_ok=True)

TABLE_PATH = TMP_DIR / "variants_table.tsv"
SCORED_PATH = TMP_DIR / "scored_variants.tsv"

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("Settings")

cancer_type = st.sidebar.selectbox(
    "Cancer Type",
    ["lung", "breast", "colon", "melanoma"]
)

# ----------------------------
# Input options
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload Annotated VCF (optional)",
    type=["vcf"]
)

run_demo = st.button("🚀 Run Demo Example (EGFR / TP53 / KRAS)")

# ----------------------------
# Helper function (SAFE subprocess)
# ----------------------------
def run_cmd(cmd):

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Pipeline failed ❌")
        st.code(result.stderr)
        st.stop()

    return result.stdout

# ----------------------------
# Select input
# ----------------------------
input_vcf = None

if uploaded_file:
    input_vcf = TMP_DIR / uploaded_file.name
    with open(input_vcf, "wb") as f:
        f.write(uploaded_file.getbuffer())

elif run_demo:
    input_vcf = INPUT_VCF

# ----------------------------
# Run pipeline
# ----------------------------
if input_vcf:

    st.info(f"Processing: {input_vcf}")

    # STEP 1: Parse VCF
    run_cmd([
        sys.executable,
        str(BASE_DIR / "scripts" / "parse_vep_to_table.py"),
        "--input",
        str(input_vcf),
        "--output",
        str(TABLE_PATH)
    ])

    # STEP 2: Evidence scoring
    run_cmd([
        sys.executable,
        str(BASE_DIR / "scripts" / "evidence_scoring.py"),
        "--table",
        str(TABLE_PATH),
        "--cancer-type",
        cancer_type,
        "--rules",
        str(RULES_FILE),
        "--out",
        str(SCORED_PATH)
    ])

    # Load results
    df = pd.read_csv(SCORED_PATH, sep="\t")

    st.success("Analysis Complete 🚀")

    # ----------------------------
    # Metrics
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Variants", len(df))
    col2.metric("Tier I", (df["tier"] == "Tier I").sum())
    col3.metric("Tier III", (df["tier"] == "Tier III").sum())

    # ----------------------------
    # Table
    # ----------------------------
    st.subheader("Variant Interpretation Table")
    st.dataframe(df, use_container_width=True)

    # ----------------------------
    # Chart
    # ----------------------------
    st.subheader("Tier Distribution")
    st.bar_chart(df["tier"].value_counts())

    # ----------------------------
    # Interpretation
    # ----------------------------
    st.subheader("Clinical Summary")

    for _, row in df.iterrows():

        gene = row["effects"].split("|")[0] if "|" in row["effects"] else row["effects"]

        st.markdown(f"""
### {gene}
- **Tier:** {row['tier']}
- **Score:** {row['score']}
- **Clinical Significance:** {row['clin_sign']}
- **Evidence:** {row['evidence']}
""")

    # ----------------------------
    # Downloads
    # ----------------------------
    st.download_button(
        "⬇️ Download TSV",
        df.to_csv(index=False, sep="\t"),
        file_name="clinical_report.tsv",
        mime="text/tab-separated-values"
    )

    st.download_button(
        "⬇️ Download JSON",
        df.to_json(orient="records", indent=2),
        file_name="clinical_report.json",
        mime="application/json"
    )

else:
    st.warning("Upload a VCF or run demo to start analysis")
