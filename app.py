import streamlit as st
import csv
import json
import io
import re

# Set up clean web page configuration
st.set_page_config(page_title="Hierarchical Risk Engine", page_icon="🛡️", layout="wide")

# =====================================================================
# DETERMINISTIC CLINICAL LEXICON (SYSTEMIC ARRAYS)
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
NEGATION_WORDS = {"no", "zero", "never", "without", "didn't", "dont", "not", "free"}

# =====================================================================
# SYSTEMIC CONTEXT PROCESSING ENGINE
# =====================================================================
def analyze_review_safety(review_text, rating):
    text_lower = review_text.lower()
    
    # Systemic Fix 1: Split text into clean, individual sentences
    sentences = re.split(r'[.,!?;\n]', text_lower)
    
    assigned_risk = "LOW"
    triggered_flag = None
    
    # Process text matching loops
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Tokenize sentence into distinct words
        words = re.findall(r'\b\w+\b', sentence)
        
        # Helper function to check for negation words right before the match
        def is_negated(target_phrase):
            phrase_words = target_phrase.split()
            # Find where the phrase starts in our token list
            for idx in range(len(words) - len(phrase_words) + 1):
                if words[idx:idx+len(phrase_words)] == phrase_words:
                    # Look back up to 3 tokens for negation markers
                    start_lookback = max(0, idx - 3)
                    for lookback_idx in range(start_lookback, idx):
                        if words[lookback_idx] in NEGATION_WORDS:
                            return True
            return False

        # Tier 1 Assessment
        for word in TIER_1_CRITICAL:
            if word in sentence and not is_negated(word):
                assigned_risk = "CRITICAL"
                triggered_flag = word
                break
                
        # Tier 2 Assessment
        if assigned_risk == "LOW":
            for word in TIER_2_HIGH:
                if word in sentence and not is_negated(word):
                    assigned_risk = "HIGH"
                    triggered_flag = word
                    break
                    
        # Tier 3 Assessment
        if assigned_risk == "LOW":
            for word in TIER_3_MEDIUM:
                if word in sentence and not is_negated(word):
                    assigned_risk = "MEDIUM"
                    triggered_flag = word
                    break
                    
        if assigned_risk != "LOW":
            break # High priority risk found, break context loops safely

    # Systemic Fix 2: Contextual Masking Logic Overhaul
    rating_val = int(rating) if str(rating).isdigit() else 0
    has_praise = any(praise_word in text_lower for praise_word in PRAISE_KEYWORDS)
    
    is_masked_risk = False
    if assigned_risk in ["CRITICAL", "HIGH"]:
        # Critical/High safety hazards are ALWAYS masked if rating is 3 or higher,
        # because standard e-commerce pipelines only check 1 and 2 stars for emergencies.
        if rating_val >= 3 or has_praise:
            is_masked_risk = True
    elif assigned_risk == "MEDIUM":
        # Medium issues follow standard threshold parameters
        if rating_val >= 4 or has_praise:
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

uploaded_file = st.file_uploader("Choose a CSV file containing reviews", type=["csv"])

if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    reader = csv.DictReader(stringio)
    
    if 'review_text' not in reader.fieldnames or 'rating' not in reader.fieldnames:
        st.error("Error: The uploaded CSV file must contain 'review_text' and 'rating' columns.")
    else:
        total_processed = 0
        total_masked_risks = 0
        display_rows = []

        for row in reader:
            total_processed += 1
            analysis = analyze_review_safety(row['review_text'], row['rating'])
            
            if analysis["masked_risk_detected"]:
                total_masked_risks += 1

            display_rows.append({
                "Review Content": row['review_text'],
                "Star Rating": row['rating'],
                "Assigned Risk Level": analysis["risk_level"],
                "Triggered Term": analysis["triggered_indicator"],
                "Masked Risk?": "⚠️ TRUE" if analysis["masked_risk_detected"] else "FALSE"
            })

        gap_percentage = round((total_masked_risks / total_processed) * 100, 2) if total_processed > 0 else 0.0

        st.markdown("---")
        st.header("📊 Executive Analysis Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Reviews Processed", value=total_processed)
        with col2:
            st.metric(label="Masked Risks Uncovered", value=total_masked_risks)
        with col3:
            st.metric(label="Data Visibility Gap (Glow Bias)", value=f"{gap_percentage}%")

        st.markdown("---")
        st.header("📋 Detailed Audit Logs")
        st.dataframe(display_rows, use_container_width=True)
