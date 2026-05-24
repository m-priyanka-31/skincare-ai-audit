import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json
import io

# Set up clean web page configuration
st.set_page_config(page_title="Automated Risk Surveillance Engine", page_icon="🛡️", layout="wide")

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
NEGATION_WORDS = {"no", "zero", "never", "without", "didn't", "dont", "not", "free"}

# =====================================================================
# SYSTEMIC PROCESSING & NEGATION CORE
# =====================================================================
def analyze_review_safety(review_text, rating=5):
    """
    Parses extracted strings using tokenized negation handling.
    Defaults rating to 5 for text-only scraped streams to evaluate maximum risk masking.
    """
    text_cleaned = review_text.lower().replace(",", " ").replace(".", " ")
    words = text_cleaned.split()
    
    assigned_risk = "LOW"
    triggered_flag = None
    
    def check_if_negated(target_word):
        if target_word in words:
            idx = words.index(target_word)
            lookback_tokens = words[max(0, idx - 2):idx]
            if any(neg.strip() in lookback_tokens for neg in NEGATION_WORDS):
                return True
        return False

    for word in TIER_1_CRITICAL:
        if word in text_cleaned and not check_if_negated(word):
            assigned_risk = "CRITICAL"
            triggered_flag = word
            break
            
    if assigned_risk == "LOW":
        for word in TIER_2_HIGH:
            if word in text_cleaned and not check_if_negated(word):
                assigned_risk = "HIGH"
                triggered_flag = word
                break
                
    if assigned_risk == "LOW":
        for word in TIER_3_MEDIUM:
            if word in text_cleaned and not check_if_negated(word):
                assigned_risk = "MEDIUM"
                triggered_flag = word
                break

    has_praise = any(praise_word in text_cleaned for praise_word in PRAISE_KEYWORDS)
    
    is_masked_risk = False
    if assigned_risk in ["CRITICAL", "HIGH", "MEDIUM"] and (has_praise or rating >= 4):
        is_masked_risk = True

    return {
        "risk_level": assigned_risk,
        "triggered_indicator": triggered_flag if triggered_flag else "None",
        "masked_risk_detected": is_masked_risk,
        "star_rating": rating
    }

# =====================================================================
# AUTOMATED DATA INGESTION LAYER (SCRAPER)
# =====================================================================
def extract_reviews_from_url(url):
    """
    Simulates enterprise agent headers to bypass standard user-agent checks
    and isolate raw paragraph blocks containing product feedback.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, f"HTTP Error Status: {response.status_code}"
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Systemic Extraction: Target common e-commerce review containers, paragraphs, and list items
        extracted_text_blocks = []
        for tag in soup.find_all(['p', 'span', 'div']):
            # Target elements that have user review keywords in their class names or content lengths
            class_str = "".join(tag.get("class", [])).lower()
            if "review" in class_str or "comment" in class_str or "text" in class_str:
                text = tag.get_text().strip()
                # Filter out menu words, structural buttons, or short clutter strings
                if len(text) > 25 and len(text) < 500 and not any(skip in text.lower() for skip in ["login", "cart", "checkout", "shipping"]):
                    if text not in extracted_text_blocks:
                        extracted_text_blocks.append(text)
                        
        # Fallback: if no specific class matches, pull all structured paragraphs
        if not extracted_text_blocks:
            extracted_text_blocks = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 30]

        return extracted_text_blocks, None
    except Exception as e:
        return None, str(e)

# =====================================================================
# STREAMLIT AUTOMATED INTERFACE
# =====================================================================
st.title("🛡️ Automated Risk Surveillance Engine")
st.subheader("Autonomous Ingestion & Clinical Extraction Pipeline")
st.write("Input any live public product URL below. The ingestion layer will automatically sandbox raw feedback blocks and route them through the priority-override data validation logic.")

# Input Field replacing the manual file uploader
target_url = st.text_input("Enter Target Product Webpage URL:", placeholder="https://example-skincare-brand.com/products/vitamin-c-serum")

if st.button("Run Autonomous Audit") and target_url:
    with st.spinner("Executing extraction agents and isolating text layers..."):
        raw_strings, error_msg = extract_reviews_from_url(target_url)
        
    if error_msg:
        st.error(f"Ingestion Aborted: {error_msg}")
        st.info("💡 Note: Highly protected networks (like Amazon) block direct client scripts. Use this field for standalone D2C brand sites, Shopify stores, or public forum endpoints during demos.")
    elif not raw_strings:
        st.warning("Ingestion Complete: No viable customer feedback strings could be isolated from the target HTML structure. Verify your URL layout.")
    else:
        # Process the dynamically scraped data array
        total_processed = 0
        total_masked_risks = 0
        display_rows = []

        for text_block in raw_strings:
            total_processed += 1
            # Automatically maps text block with placeholder 5-star rating to isolate risk concealment
            analysis = analyze_review_safety(text_block, rating=5)
            
            if analysis["masked_risk_detected"]:
                total_masked_risks += 1

            display_rows.append({
                "Extracted Text Block": text_block,
                "Assigned Risk Level": analysis["risk_level"],
                "Triggered Indicator": analysis["triggered_indicator"],
                "Masked Risk Alert": "⚠️ CRITICAL MASKED RISK" if analysis["risk_level"] in ["CRITICAL", "HIGH"] else ("MEDIUM RISK" if analysis["risk_level"] == "MEDIUM" else "CLEAN/SAFE")
            })

        gap_percentage = round((total_masked_risks / total_processed) * 100, 2) if total_processed > 0 else 0.0

        # Executive Statistics Rendering
        st.markdown("---")
        st.header("📊 Live Risk Audit Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Text Blocks Isolated", value=total_processed)
        with col2:
            st.metric(label="Masked Risks Identified", value=total_masked_risks)
        with col3:
            st.metric(label="Data Visibility Gap Metrics", value=f"{gap_percentage}%")

        st.markdown("---")
        st.header("📋 Automated Audit Logs (Real-Time Stream)")
        st.dataframe(display_rows, use_container_width=True)
