from pathlib import Path

import pandas as pd


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# INPUT FILE
# ==========================================

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "prospectivity_scores.csv"
)


# ==========================================
# OUTPUT FILE
# ==========================================

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "exploration_recommendations.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

print("\nADDING EXPLORATION RECOMMENDATIONS")

print("\nLOADING PROSPECTIVITY DATA...")


df = pd.read_csv(INPUT_FILE)


print(f"\nTOTAL ZONES: {len(df)}")


# ==========================================
# EVIDENCE LEVEL FUNCTION
# ==========================================

def get_evidence_level(score):

    if score >= 0.70:
        return "STRONG"

    elif score >= 0.40:
        return "MODERATE"

    else:
        return "WEAK"


# ==========================================
# EXPLANATION FUNCTION
# ==========================================

def generate_explanation(row):

    reasons = []


    # --------------------------------------
    # MANGANESE PROXIMITY
    # --------------------------------------

    proximity_level = get_evidence_level(
        row["MN_PROXIMITY_SCORE"]
    )


    if proximity_level == "STRONG":

        reasons.append(
            "Strong proximity to known manganese occurrence evidence"
        )

    elif proximity_level == "MODERATE":

        reasons.append(
            "Moderate proximity to known manganese occurrence evidence"
        )

    else:

        reasons.append(
            "Limited proximity to known manganese occurrence evidence"
        )


    # --------------------------------------
    # SPECTRAL EVIDENCE
    # --------------------------------------

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


    # --------------------------------------
    # TERRAIN EVIDENCE
    # --------------------------------------

    terrain_level = get_evidence_level(
        row["TERRAIN_SCORE"]
    )


    if terrain_level == "STRONG":

        reasons.append(
            "Strong terrain characteristics for exploration prioritization"
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
# RECOMMENDATION FUNCTION
# ==========================================

def generate_recommendation(priority):

    if priority == "HIGH":

        return (
            "Prioritize detailed geological mapping, "
            "ground validation, and targeted sampling."
        )


    elif priority == "MODERATE":

        return (
            "Conduct preliminary field reconnaissance "
            "and geological validation before further investment."
        )


    elif priority == "LOW":

        return (
            "Maintain as a lower-priority area. "
            "Reassess when additional geological evidence becomes available."
        )


    else:

        return (
            "Review available evidence before exploration planning."
        )


# ==========================================
# CONFIDENCE FUNCTION
# ==========================================

def calculate_confidence(row):

    evidence_scores = [

        row["SPECTRAL_SCORE"],

        row["TERRAIN_SCORE"],

        row["MN_PROXIMITY_SCORE"]

    ]


    confidence = (
        sum(evidence_scores)
        / len(evidence_scores)
    ) * 100


    return round(
        confidence,
        2
    )


# ==========================================
# APPLY FUNCTIONS
# ==========================================

print("\nGENERATING ZONE EXPLANATIONS...")


df["EXPLANATION"] = df.apply(

    generate_explanation,

    axis=1

)


print("\nGENERATING RECOMMENDATIONS...")


df["RECOMMENDATION"] = df[

    "PRIORITY"

].apply(

    generate_recommendation

)


print("\nCALCULATING EVIDENCE CONFIDENCE...")


df["EVIDENCE_CONFIDENCE"] = df.apply(

    calculate_confidence,

    axis=1

)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\nFIRST 10 RESULTS:\n")


print(

    df[

        [

            "zone_id",

            "PROSPECTIVITY_SCORE",

            "PRIORITY",

            "EVIDENCE_CONFIDENCE",

            "EXPLANATION",

            "RECOMMENDATION"

        ]

    ]

    .head(10)

    .to_string(

        index=False

    )

)


# ==========================================
# SAVE OUTPUT
# ==========================================

df.to_csv(

    OUTPUT_FILE,

    index=False

)


print("\nSAVED:")

print(OUTPUT_FILE)


print("\nSUCCESS!")

print(
    "Zone explanations and recommendations added successfully."
)