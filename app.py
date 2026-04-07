import streamlit as st

# --- THE ENGINE ---
def analyze_review(text):
    text = text.lower()
    # Corrected Lists to include "Stripped" and "Harsh"
    emergency = ['stuck', 'doctor', 'emergency', 'blind', 'scared', 'pain']
    medical = ['eczema', 'rash', 'burn', 'swollen', 'itchy', 'break out', 'redness', 'stings', 'stripped', 'irritated']
    education = ['how to', 'confused', 'order', 'step', 'every day']
    quality = ['pump', 'broken', 'leaked', 'empty', 'smell', 'texture', 'watery', 'harsh', 'dryness']

    # CRITICAL: Ensure these 4 lines below have EXACTLY 4 spaces of indentation
    if any(word in text for word in emergency): 
        return "🆘 EMERGENCY: Legal/Safety Risk"
    elif any(word in text for word in medical): 
        return "🚨 MEDICAL: Adverse Reaction"
    elif any(word in text for word in education): 
        return "📘 EDUCATION: Usage Confusion"
    elif any(word in text for word in quality):
        return "⚠️ QUALITY: Formula/Packaging Issue"
    else: 
        return "✅ ROUTINE: Brand Engagement"

# --- THE USER INTERFACE ---
st.set_page_config(page_title="Skincare Risk Audit AI", page_icon="🧪")
st.title("🧪 Skincare Sentiment & Risk Engine")
st.markdown("### Professional Audit Tool for High-Growth Brands")

# Input Section
user_input = st.text_area("Paste a Customer Review here to Audit:", 
                          placeholder="e.g., My eyes are swollen and burning after using the serum...")

if st.button("Run Audit"):
    if user_input:
        result = analyze_review(user_input)
        
        # Visual Feedback
        if "EMERGENCY" in result:
            st.error(result)
            st.warning("Action Required: Alert Legal and Product Safety Teams immediately.")
        elif "MEDICAL" in result:
            st.error(result)
        elif "EDUCATION" in result:
            st.info(result)
        elif "QUALITY" in result:
            st.warning(result)
        else:
            st.success(result)
            
        st.write(f"**Analysis for:** '{user_input[:50]}...'")
    else:
        st.write("Please enter a review to analyze.")

st.sidebar.markdown("### Brand Portfolio: The INKEY List")
st.sidebar.write("Currently Monitoring: Multi-Peptide Eye Serum")
