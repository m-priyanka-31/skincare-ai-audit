import streamlit as st
import csv
import json
import io

# Set up clean web page configuration
st.set_page_config(page_title="Hierarchical Risk Engine", page_icon="🛡️", layout="wide")

# =====================================================================
# DETERMINISTIC CLINICAL LEXICON
# =====================================================================
TIER_1_CRITICAL = [
    "stinging", "burning", "burns", "chemical burn", "raw skin", "peeling skin",
    "bleeding", "blisters", "oozing", "pus", "swelling", "inflammation", 
    "edema", "erythema", "crusting", "scabbing", "skin peel", "damaged barrier", 
    "sensitized", "painful", "hurts", "throbbing", "tender to touch"
]

TIER_2_HIGH = [
    "rash", "hives", "welts", "allergic", "allergy", "contact dermatitis", 
    "itching", "itchy", "red spots", "bumps", "swelled up", "breakout", 
    "swollen eyes", "dermatitis", "irritated", "irritation"
]

TIER_3_MEDIUM = [
    "cystic acne", "nodules", "painful bumps", "pus pimples", "clogged pores", 
    "blackheads", "whiteheads", "severe breakout", "ruined my face", "scarring", 
    "worsened pigment", "caused dark spots", "skin darkened", "left marks"
]

PRAISE_KEYWORDS = ["glow", "effective", "good", "nice", "love", "radiant", "awesome", "best"]

# =====================================================================
# ENGINE LOGIC
# =====================================================================
def analyze_review_safety(review_text, rating):
    text_lower = review_text.lower()
    assigned_risk = "LOW"
    triggered_flag = None
    
    for word in TIER_1_CRITICAL:
        if word in text_lower:
            assigned_risk = "CRITICAL"
            triggered_flag = word
            break
            
    if assigned_risk == "LOW":
        for word in TIER_2_HIGH:
            if word in text_lower:
                assigned_risk = "HIGH"
                triggered_flag = word
                break
                
    if assigned_risk == "LOW":
        for word in TIER_3_MEDIUM:
            if word in text_lower:
                assigned_risk = "MEDIUM"
                triggered_flag = word
                break

    has_praise = any(praise_word in text_lower for praise_word in PRAISE_KEYWORDS)
    is_high_rating = int(rating) >= 4 if str(rating).isdigit() else False
    
    is_masked_risk = False
    if assigned_risk in ["CRITICAL", "HIGH", "MEDIUM"] and (has_praise or is_high_rating):
        is_masked_risk = True

    return {
        "risk_level": assigned_risk,
        "triggered_indicator": triggered_flag if triggered_flag else "None",
        "masked_risk_detected": is_masked_risk,
        "star_rating": rating
    }

# =====================================================================
# STREAMLIT USER INTERFACE
# =====================================================================
st.title("🛡️ Contextual Risk Surveillance Engine")
st.subheader("Identifying Masked Safety Risks Hidden in D2C Feedback Pipelines")
st.write("Upload a raw customer feedback CSV dataset to extract underlying physiological risks and calculate your brand's data gap.")

# 1. File Uploader Component
uploaded_file = st.file_uploader("Choose a CSV file containing reviews", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV directly from browser memory
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    reader = csv.DictReader(stringio)
    
    if 'review_text' not in reader.fieldnames or 'rating' not in reader.fieldnames:
        st.error("Error: The uploaded CSV file must contain 'review_text' and 'rating' columns.")
    else:
        # Initialize processing metrics
        total_processed = 0
        critical_flags = 0
        high_flags = 0
        medium_flags = 0
        low_flags = 0
        total_masked_risks = 0
        display_rows = []

        for row in reader:
            total_processed += 1
            analysis = analyze_review_safety(row['review_text'], row['rating'])
            
            if analysis["risk_level"] == "CRITICAL": critical_flags += 1
            elif analysis["risk_level"] == "HIGH": high_flags += 1
            elif analysis["risk_level"] == "MEDIUM": medium_flags += 1
            else: low_flags += 1
            
            if analysis["masked_risk_detected"]:
                total_masked_risks += 1

            # Format rows for visual browser display table
            display_rows.append({
                "Review Content": row['review_text'],
                "Star Rating": row['rating'],
                "Assigned Risk Level": analysis["risk_level"],
                "Triggered Term": analysis["triggered_indicator"],
                "Masked Risk?": "⚠️ TRUE" if analysis["masked_risk_detected"] else "FALSE"
            })

        gap_percentage = round((total_masked_risks / total_processed) * 100, 2) if total_processed > 0 else 0.0

        # 2. Display Executive Metrics Grid
        st.markdown("---")
        st.header("📊 Executive Analysis Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Reviews Processed", value=total_processed)
        with col2:
            st.metric(label="Masked Risks Uncovered", value=total_masked_risks)
        with col3:
            st.metric(label="Data Visibility Gap (Glow Bias)", value=f"{gap_percentage}%")

        # 3. Display Detailed Breakdowns
        st.markdown("---")
        st.header("📋 Detailed Audit Logs")
        st.dataframe(display_rows, use_container_width=True)
