
import streamlit as st
import pandas as pd
import subprocess
import json
from pathlib import Path

st.set_page_config(
    page_title="Clinical Somatic Variant Interpreter",
    layout="wide"
)

st.title("🧬 Clinical Somatic Variant Interpretation")

st.markdown("""
Automated AMP/ASCO/CAP-inspired somatic variant interpretation workflow.

Upload an annotated VCF and generate:
- Clinical evidence scoring
- Somatic tier classification
- Downloadable reports
""")

Path("tmp").mkdir(exist_ok=True)

st.sidebar.header("Configuration")

cancer_type = st.sidebar.selectbox(
    "Cancer Type",
    ["lung", "breast", "colon", "melanoma"]
)

uploaded_file = st.file_uploader(
    "Upload Annotated VCF",
    type=["vcf"]
)

demo_button = st.button("Run Demo Example")

input_vcf = None

if uploaded_file:

    input_vcf = f"tmp/{uploaded_file.name}"

    with open(input_vcf, "wb") as f:
        f.write(uploaded_file.getbuffer())

elif demo_button:

    input_vcf = "example_data/demo.vep.vcf"

if input_vcf:

    if st.button("Run Clinical Interpretation") or demo_button:

        with st.spinner("Running pipeline..."):

            subprocess.run([
                "python",
                "scripts/parse_vep_to_table.py",
                "--input",
                input_vcf,
                "--output",
                "tmp/variants_table.tsv"
            ], check=True)

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

        scored = pd.read_csv(
            "tmp/scored_variants.tsv",
            sep="\t"
        )

        st.success("Interpretation Complete")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Variants",
            len(scored)
        )

        col2.metric(
            "Tier I Variants",
            (scored["tier"] == "Tier I").sum()
        )

        col3.metric(
            "Tier III Variants",
            (scored["tier"] == "Tier III").sum()
        )

        st.subheader("Clinical Variant Interpretation")

        st.dataframe(
            scored,
            use_container_width=True
        )

        st.subheader("Tier Distribution")

        tier_counts = scored["tier"].value_counts()

        st.bar_chart(tier_counts)

        st.subheader("Clinical Interpretation Summary")

        for _, row in scored.iterrows():

            gene = row["effects"].split("|")[0]

            st.markdown(
                f"""
                ### {gene}
                - Tier: **{row['tier']}**
                - Score: **{row['score']}**
                - Clinical Significance: **{row['clin_sign']}**
                - Evidence: **{row['evidence']}**
                """
            )

        json_report = scored.to_json(
            orient="records",
            indent=2
        )

        st.download_button(
            "Download JSON Report",
            json_report,
            file_name="clinical_report.json",
            mime="application/json"
        )

        st.download_button(
            "Download TSV Report",
            scored.to_csv(sep="\t", index=False),
            file_name="clinical_report.tsv",
            mime="text/tab-separated-values"
        )
