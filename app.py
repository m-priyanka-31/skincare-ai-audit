import streamlit as st
import pandas as pd

# --- THE "MILLION-DOLLAR" ENGINE ---
def analyze_review(text):
    text = str(text).lower()
    
    # Level 1: Legal/Safety Emergency (Panic & Doctor mentions)
    emergency = [
        'stuck', 'doctor', 'emergency', 'clinic', 'hospital', 
        'blind', 'scared', 'concerned', 'pain', 'don\'t know what to do',
        'help', 'urgent', 'ophthalmologist', 'emergency room', 'er'
    ]
    
    # Level 2: Adverse Reaction (Symptoms)
    medical = [
        'eczema', 'rash', 'burn', 'swollen', 'itchy', 'break out', 
        'redness', 'stings', 'stripped', 'irritated', 'puffy', 
        'puffiness', 'hives', 'blisters', 'allergy', 'reaction', 'blotchiness'
    ]
    
    # Level 3: Education Gaps (Usage Confusion)
    education = [
        'how to', 'confused', 'order', 'step', 'every day', 
        'twice', 'shake', 'layer', 'mix with'
    ]
    
    # Level 4: Quality/Retention Risks
    quality = [
        'pump', 'broken', 'leaked', 'empty', 'smell', 'texture', 
        'watery', 'harsh', 'dryness', 'waste', 'disappointed'
    ]

    if any(word in text for word in emergency): 
        return "🆘 EMERGENCY: High Legal Risk"
    elif any(word in text for word in medical): 
        return "🚨 MEDICAL: Adverse Reaction"
    elif any(word in text for word in education): 
        return "📘 EDUCATION: Usage Confusion"
    elif any(word in text for word in quality):
        return "⚠️ QUALITY: Retention Risk"
    else: 
        return "✅ ROUTINE: Brand Engagement"

# --- THE USER INTERFACE ---
st.set_page_config(page_title="Skincare Risk Audit Pro", layout="wide", page_icon="🧪")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Skincare Risk Audit: Enterprise Edition")
st.markdown("Automated Safety & Retention Monitoring for High-Growth Brands")

# --- SIDEBAR: SINGLE REVIEW TESTER ---
st.sidebar.header("Quick Audit")
single_input = st.sidebar.text_area("Paste a single review to test the AI:")
if st.sidebar.button("Run Quick Audit"):
    if single_input:
        res = analyze_review(single_input)
        if "EMERGENCY" in res or "MEDICAL" in res:
            st.sidebar.error(res)
        elif "ROUTINE" in res:
            st.sidebar.success(res)
        else:
            st.sidebar.warning(res)
    else:
        st.sidebar.write("Please enter text.")

# --- MAIN: BULK DATA PIPELINE ---
st.header("Bulk Data Analysis")
st.write("Upload your customer feedback (CSV or Excel) to generate a Risk Distribution Report.")

uploaded_file = st.file_uploader("Upload file (Must have a column named 'review')", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Handle File Types
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if 'review' in df.columns:
            # Processing
            with st.spinner('AI is auditing reviews...'):
                df['Risk Level'] = df['review'].apply(analyze_review)
            
            st.success("Audit Complete!")

            # Metric Dashboard
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Reviews", len(df))
            m2.metric("Safety Risks", len(df[df['Risk Level'].str.contains('🆘|🚨')]))
            m3.metric("Education Gaps", len(df[df['Risk Level'].str.contains('📘')]))
            m4.metric("Retention Risks", len(df[df['Risk Level'].str.contains('⚠️')]))

            # Data Table
            st.subheader("Detailed Audit Log")
            st.dataframe(df, use_container_width=True)
            
            # Export
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📩 Download Final Audit Report", csv, "Brand_Risk_Audit.csv", "text/csv")
            
        else:
            st.error("Error: The file must contain a column named exactly 'review'.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.divider()
st.caption("Developed for High-Growth Skincare Founders. Confidential Risk Engine v3.0")
