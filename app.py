import streamlit as st
import pandas as pd
from classifier import classify_jd
import os

st.set_page_config(page_title="JD Triage App", layout="wide")

st.title("JD Triage App")

st.markdown("Paste a job description below")

jd_text = st.text_area("Job Description", height=300)

if st.button("Analyze Job"):
    if jd_text.strip():

        result = classify_jd(jd_text)

        st.subheader("Results")

        st.write(f"Bucket: {result['bucket']}")
        st.write(f"Tier: {result['tier']}")
        st.write(f"Decision: {result['decision']}")
        st.write(f"Sponsorship Flag: {result['sponsorship_flag']}")
        st.write(f"Keywords Found: {result['tech_keywords']}")

        data = {
            "Bucket": [result['bucket']],
            "Tier": [result['tier']],
            "Decision": [result['decision']],
            "Sponsorship": [result['sponsorship_flag']],
            "Keywords": [result['tech_keywords']]
        }

        df = pd.DataFrame(data)

        file_exists = os.path.isfile("results.csv")

        df.to_csv(
            "results.csv",
            mode='a',
            header=not file_exists,
            index=False
        )

        st.success("Saved to results.csv")