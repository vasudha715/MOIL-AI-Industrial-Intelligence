def get_evidence_level(score):

    if score >= 0.70:

        return "STRONG"

    elif score >= 0.40:

        return "MODERATE"

    else:

        return "WEAK"


# ==========================================
# GENERATE EXPLANATION
# ==========================================

def generate_explanation(row):

    reasons = []


    # ======================================
    # MANGANESE PROXIMITY
    # ======================================

    proximity_level = get_evidence_level(

        row["MN_PROXIMITY_SCORE"]

    )


    if proximity_level == "STRONG":

        reasons.append(

            "Strong proximity to known manganese "
            "occurrence evidence"

        )


    elif proximity_level == "MODERATE":

        reasons.append(

            "Moderate proximity to known manganese "
            "occurrence evidence"

        )


    else:

        reasons.append(

            "Limited proximity to known manganese "
            "occurrence evidence"

        )


    # ======================================
    # SPECTRAL EVIDENCE
    # ======================================

    spectral_level = get_evidence_level(

        row["SPECTRAL_SCORE"]

    )


    if spectral_level == "STRONG":

        reasons.append(

            "Strong satellite spectral anomaly evidence"

        )


    elif spectral_level == "MODERATE":

        reasons.append(

            "Moderate satellite spectral evidence"

        )


    else:

        reasons.append(

            "Weak satellite spectral evidence"

        )


    # ======================================
    # TERRAIN EVIDENCE
    # ======================================

    terrain_level = get_evidence_level(

        row["TERRAIN_SCORE"]

    )


    if terrain_level == "STRONG":

        reasons.append(

            "Strong terrain characteristics for "
            "exploration prioritization"

        )


    elif terrain_level == "MODERATE":

        reasons.append(

            "Moderate terrain evidence"

        )


    else:

        reasons.append(

            "Limited terrain evidence"

        )


    return "; ".join(reasons)


# ==========================================
# GENERATE RECOMMENDATION
# ==========================================

def generate_recommendation(priority):

    if priority == "VERY HIGH":

        return (

            "Highest-priority area for detailed "
            "geological mapping, ground validation, "
            "and targeted sampling."

        )


    elif priority == "HIGH":

        return (

            "Prioritize detailed geological mapping, "
            "ground validation, and targeted sampling."

        )


    elif priority == "MODERATE":

        return (

            "Conduct preliminary field reconnaissance "
            "and geological validation before further "
            "investment."

        )


    elif priority == "LOW":

        return (

            "Maintain as a lower-priority area. "
            "Reassess when additional geological "
            "evidence becomes available."

        )


    else:

        return (

            "Review available evidence before "
            "exploration planning."

        )


# ==========================================
# CALCULATE EVIDENCE CONFIDENCE
# ==========================================

def calculate_confidence(row):

    evidence_scores = [

        row["SPECTRAL_SCORE"],

        row["TERRAIN_SCORE"],

        row["MN_PROXIMITY_SCORE"]

    ]


    confidence = (

        sum(evidence_scores)

        /

        len(evidence_scores)

    ) * 100


    return round(

        confidence,

        2

    )


# ==========================================
# ADD RECOMMENDATIONS
# ==========================================

def add_recommendations(dataframe):

    df = dataframe.copy()


    # ======================================
    # EXPLANATIONS
    # ======================================

    df["EXPLANATION"] = df.apply(

        generate_explanation,

        axis=1

    )


    # ======================================
    # RECOMMENDATIONS
    # ======================================

    df["RECOMMENDATION"] = (

        df["PRIORITY"]

        .apply(

            generate_recommendation

        )

    )


    # ======================================
    # EVIDENCE CONFIDENCE
    # ======================================

    df["EVIDENCE_CONFIDENCE"] = (

        df.apply(

            calculate_confidence,

            axis=1

        )

    )


    return df