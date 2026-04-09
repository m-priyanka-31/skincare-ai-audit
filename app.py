import streamlit as st
import pandas as pd

# --- THE ENGINE ---
def analyze_review(text):
    text = str(text).lower()
    
    # 1. EMERGENCY (Safety/Legal)
    emergency = [
        'doctor', 'hospital', 'emergency', 'pain', 'allergic reaction',
        'emergencia', 'dolor', 'reacción alérgica',
        'medico', 'ospedale', 'pronto soccorso' # Italian additions
    ]
    
    # 2. MEDICAL (Symptoms)
    medical = [
        'burn', 'red', 'puffy', 'rash', 'swollen', 'break out', 
        'stings', 'irritation', 'irritate', 'allergy',
        'quemadura', 'rojo', 'hinchado', 'irritación', 'alergia',
        'brucia', 'rossore', 'gonfio', 'irritazione', 'brufoli' # Italian additions
    ]
    
    # 3. EDUCATION (Usage Confusion)
    education = [
        'how to', 'confused', 'order', 'step', 'every day', 'shake',
        'como usar', 'confundido', 'paso',
        'come usare', 'confuso' # Italian additions
    ]
    
    # 4. QUALITY (Product/Packaging)
    quality = [
        'broken', 'leaked', 'empty', 'smell', 'texture', 'harsh', 'amount',
        'roto', 'vacío', 'olor', 'textura', 'cantidad',
        'rotto', 'vuoto', 'odore', 'poca' # Italian additions
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

st.title("🧪 Skincare Risk Audit: Enterprise Edition")
st.markdown("Automated Safety & Retention Monitoring for Global Brands")

# --- SIDEBAR: QUICK TEST ---
st.sidebar.header("Quick Audit")
single_input = st.sidebar.text_area("Paste a review to test (English, Spanish, or Italian):")
if st.sidebar.button("Run Quick Audit"):
    if single_input:
        res = analyze_review(single_input)
        st.sidebar.info(res)

# --- MAIN: BULK DATA ---
st.header("Bulk Data Analysis")
uploaded_file = st.file_uploader("Upload CSV or Excel (Must have 'review' column)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if 'review' in df.columns:
            df['Risk Level'] = df['review'].apply(analyze_review)
            
            # --- METRICS ---
            st.success("Audit Complete!")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Reviews", len(df))
            m2.metric("Safety Risks 🚨", len(df[df['Risk Level'].str.contains('🆘|🚨')]))
            m3.metric("Education Gaps 📘", len(df[df['Risk Level'].str.contains('📘')]))
            m4.metric("Retention Risks ⚠️", len(df[df['Risk Level'].str.contains('⚠️')]))

            # --- VISUAL HEATMAP ---
            st.divider()
            st.subheader("🔥 Risk Distribution Analysis")
            risk_counts = df['Risk Level'].value_counts()
            # Professional red chart for safety visibility
            st.bar_chart(risk_counts, color="#FF4B4B")
            st.info("Concentration of Legal, Medical, and Retention risks across global feedback.")

            # --- DATA LOG ---
            st.subheader("📋 Executive Priority Log")
            priority_df = df.sort_values(by='Risk Level', ascending=False)
            st.dataframe(priority_df, width='stretch')
            
            # --- DOWNLOAD ---
            st.divider()
            st.markdown("### 📥 Export for Stakeholders")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📩 Download Executive Audit Report (.CSV)",
                data=csv,
                file_name='Brand_Risk_Audit_2026.csv',
                mime='text/csv'
            )
        else:
            st.error("Error: Column 'review' not found in your file.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
