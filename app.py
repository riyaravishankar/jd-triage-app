import streamlit as st
import pandas as pd
from classifier import classify_jd
import os
from datetime import datetime

st.set_page_config(page_title="JD Triage App", layout="wide")

st.title("JD Triage App")

jd_text = st.text_area("Paste Job Description", height=300)

company = st.text_input("Company")
role = st.text_input("Role")
job_link = st.text_input("Job Link")

if st.button("Analyze Job"):

if jd_text.strip():

    result = classify_jd(jd_text)

    st.subheader("Results")

    st.success(f"Bucket: {result['bucket']}")
    st.info(f"Tier: {result['tier']}")
    st.write(f"Decision: {result['decision']}")
    st.write(f"Resume Version: {result['resume_version']}")
    st.write(f"ATS Match: {result['ats_match']}%")
    st.write(f"Sponsorship Risk: {result['sponsorship_risk']}")
    st.write(f"Technical Intensity: {result['technical_intensity']}")
    st.write(f"Keywords Found: {result['tech_keywords']}")
    st.write(f"Suggested Search Terms: {result['search_terms']}")

    data = {
        "Date": [datetime.today().strftime('%Y-%m-%d')],
        "Company": [company],
        "Role": [role],
        "Job Link": [job_link],
        "Bucket": [result['bucket']],
        "Tier": [result['tier']],
        "Resume Version": [result['resume_version']],
        "ATS Match %": [result['ats_match']],
        "Applied": [""],
        "OA": [""],
        "Interview Stage": [""],
        "Status": [result['decision']],
        "Notes": [""]
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
