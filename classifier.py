from keywords import BUCKET_KEYWORDS, SPONSORSHIP_RED_FLAGS, TECH_KEYWORDS


def classify_jd(text):

    text = text.lower()

    bucket_scores = {}

    for bucket, keywords in BUCKET_KEYWORDS.items():
        score = sum(keyword in text for keyword in keywords)
        bucket_scores[bucket] = score

    best_bucket = max(bucket_scores, key=bucket_scores.get)

    sponsorship_flag = any(flag in text for flag in SPONSORSHIP_RED_FLAGS)

    tech_found = [kw for kw in TECH_KEYWORDS if kw in text]

    if sponsorship_flag:
        tier = "C"
        decision = "SKIP"
        sponsorship_risk = "High"

    elif bucket_scores[best_bucket] >= 3:
        tier = "A"
        decision = "APPLY"
        sponsorship_risk = "Low"

    elif bucket_scores[best_bucket] >= 1:
        tier = "B"
        decision = "APPLY"
        sponsorship_risk = "Medium"

    else:
        tier = "C"
        decision = "SKIP"
        sponsorship_risk = "Unknown"

    if any(word in text for word in ["spark", "docker", "airflow", "dbt", "databricks"]):
        technical_intensity = "High"

    elif any(word in text for word in ["python", "sql", "tableau", "power bi"]):
        technical_intensity = "Medium"

    else:
        technical_intensity = "Low"

    resume_map = {
        "General Analyst": "General Analyst",
        "Healthcare Analytics": "Healthcare",
        "BI / Reporting": "BI / Reporting",
        "Operations & Business": "Operations & Business",
        "Product & Program": "Product / Program / Technical"
    }

    search_terms = {
        "General Analyst": [
            "Insights Analyst",
            "Reporting Analyst",
            "Decision Support Analyst"
        ],

        "Healthcare Analytics": [
            "Healthcare Analyst",
            "Clinical Reporting Analyst",
            "Health Informatics Analyst"
        ],

        "BI / Reporting": [
            "Dashboard Analyst",
            "BI Associate",
            "Reporting Specialist"
        ],

        "Operations & Business": [
            "Operations Analyst",
            "Continuous Improvement Analyst",
            "Business Operations Associate"
        ],

        "Product & Program": [
            "Program Analyst",
            "PMO Analyst",
            "Implementation Analyst"
        ]
    }

    ats_match = min(bucket_scores[best_bucket] * 20 + len(tech_found) * 5, 95)

    return {
        "bucket": best_bucket,
        "tier": tier,
        "decision": decision,
        "sponsorship_risk": sponsorship_risk,
        "technical_intensity": technical_intensity,
        "resume_version": resume_map[best_bucket],
        "ats_match": ats_match,
        "tech_keywords": ", ".join(tech_found),
        "search_terms": ", ".join(search_terms[best_bucket])
    }
