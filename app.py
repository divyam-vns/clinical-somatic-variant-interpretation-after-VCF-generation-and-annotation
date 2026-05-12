
import streamlit as st
import pandas as pd
import subprocess
from pathlib import Path

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="Clinical Somatic Variant Interpreter",
    layout="wide"
)

st.title("🧬 Clinical Somatic Variant Interpretation Pipeline")

st.markdown("""
This app performs **AMP/ASCO/CAP-inspired somatic variant interpretation**:

- VCF parsing (VEP/ANN-style annotations)
- Evidence-based scoring
- Clinical tier classification
- Downloadable structured reports
""")

# ----------------------------
# Create required folders
# ----------------------------
Path("tmp").mkdir(exist_ok=True)

# ----------------------------
# Sidebar config
# ----------------------------
st.sidebar.header("Configuration")

cancer_type = st.sidebar.selectbox(
    "Cancer Type",
    ["lung", "breast", "colon", "melanoma"]
)

# ----------------------------
# Inputs
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload Annotated VCF (optional)",
    type=["vcf"]
)

run_demo = st.button("🚀 Run Demo Example (EGFR / TP53 / KRAS)")

input_vcf = None

# ----------------------------
# Handle input source
# ----------------------------
if uploaded_file:
    input_vcf = f"tmp/{uploaded_file.name}"

    with open(input_vcf, "wb") as f:
        f.write(uploaded_file.getbuffer())

elif run_demo:
    input_vcf = "example_data/demo.vep.vcf"

# ----------------------------
# Pipeline Execution
# ----------------------------
if input_vcf:

    st.info(f"Processing: {input_vcf}")

    # Step 1: Parse VCF
    subprocess.run([
        "python",
        "scripts/parse_vep_to_table.py",
        "--input",
        input_vcf,
        "--output",
        "tmp/variants_table.tsv"
    ], check=True)

    # Step 2: Evidence Scoring
    subprocess.run([
        "python",
        "scripts/evidence_scoring.py",
        "--table",
        "tmp/variants_table.tsv",
        "--cancer-type",
        cancer_type,
        "--rules",
        "resources/amp_guidelines.yaml",
        "--out",
        "tmp/scored_variants.tsv"
    ], check=True)

    # ----------------------------
    # Load results
    # ----------------------------
    df = pd.read_csv("tmp/scored_variants.tsv", sep="\t")

    st.success("Analysis Complete 🚀")

    # ----------------------------
    # Metrics
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Variants", len(df))
    col2.metric("Tier I Variants", (df["tier"] == "Tier I").sum())
    col3.metric("Tier III Variants", (df["tier"] == "Tier III").sum())

    # ----------------------------
    # Table view
    # ----------------------------
    st.subheader("🧬 Clinical Variant Table")

    st.dataframe(df, use_container_width=True)

    # ----------------------------
    # Tier distribution
    # ----------------------------
    st.subheader("📊 Tier Distribution")

    st.bar_chart(df["tier"].value_counts())

    # ----------------------------
    # Gene-level interpretation
    # ----------------------------
    st.subheader("🔬 Clinical Interpretation Summary")

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
    st.subheader("⬇️ Download Reports")

    st.download_button(
        "Download TSV",
        df.to_csv(index=False, sep="\t"),
        file_name="clinical_report.tsv",
        mime="text/tab-separated-values"
    )

    st.download_button(
        "Download JSON",
        df.to_json(orient="records", indent=2),
        file_name="clinical_report.json",
        mime="application/json"
    )

else:
    st.warning("Upload a VCF file or run the demo to start analysis.")
