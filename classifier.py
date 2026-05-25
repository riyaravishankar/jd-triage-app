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
        tier = "T3"
        decision = "SKIP"
    elif bucket_scores[best_bucket] >= 3:
        tier = "T1"
        decision = "APPLY"
    elif bucket_scores[best_bucket] >= 1:
        tier = "T2"
        decision = "APPLY"
    else:
        tier = "T3"
        decision = "SKIP"

    return {
        "bucket": best_bucket,
        "tier": tier,
        "decision": decision,
        "sponsorship_flag": sponsorship_flag,
        "tech_keywords": ", ".join(tech_found)
    }