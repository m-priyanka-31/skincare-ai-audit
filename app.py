import streamlit as st
import pandas as pd
import re

# --- THE UPDATED RISK ENGINE ---
def analyze_review(text):
    text = str(text).lower()
    
    # 0. THE CONTEXTUAL FIX: Keywords that often mask safety issues
    masking_keywords = ['glow', 'glowing', 'radiant', 'shimmer', 'bright', 'glass skin']
    has_glow = any(mask in text for mask in masking_keywords)

    # 1. EMERGENCY (Safety/Legal) - Global Lexicon
    emergency = [
        'doctor', 'hospital', 'emergency', 'pain', 'allergic reaction',
        'emergencia', 'dolor', 'reacción alérgica',
        'medico', 'ospedale', 'pronto soccorso', 'reazione allergica'
    ]
    
    # 2. MEDICAL (Symptoms) - Global Lexicon
    medical = [
        'burn', 'red', 'puffy', 'rash', 'swollen', 'break out', 'hot',
        'stings', 'irritation', 'irritate', 'allergy', 'itchy',
        'quemadura', 'rojo', 'hinchado', 'irritación', 'alergia', 'ardor', 'picazón',
        'brucia', 'rossore', 'gonfio', 'irritazione', 'brufoli', 'prurito'
    ]
    
    # 3. EDUCATION (Usage Confusion)
    education = [
        'how to', 'confused', 'order', 'step', 'every day', 'shake',
        'como usar', 'confundido', 'paso',
        'come usare', 'confuso'
    ]
    
    # 4. QUALITY (Product/Packaging)
    quality = [
        'broken', 'leaked', 'empty', 'smell', 'texture', 'harsh', 'amount',
        'roto', 'vacío', 'olor', 'textura', 'cantidad',
        'rotto', 'vuoto', 'odore', 'poca'
    ]

    # --- PRIORITY LOGIC ---
    if any(word in text for word in emergency): 
        return "🆘 EMERGENCY: High Legal Risk"
    
    # THE PIVOT: If glowing is mentioned WITH medical symptoms, it's a Critical Risk
    elif has_glow and any(word in text for word in medical):
        return "🔴 CRITICAL: Masked Adverse Reaction"
        
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
st.markdown("### Automated Safety & Retention Monitoring for Global Brands")

# --- SIDEBAR: QUICK TEST ---
st.sidebar.header("Quick Audit")
st.sidebar.info("Test for the 'Glowing Bias' or Global Lexicons here.")
single_input = st.sidebar.text_area("Paste a review (EN, ES, IT):")
if st.sidebar.button("Run Quick Audit"):
    if single_input:
        res = analyze_review(single_input)
        st.sidebar.markdown(f"**Result:** {res}")

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
            # Count both Emergency and Critical Masked Reactions as Safety Risks
            safety_count = len(df[df['Risk Level'].str.contains('🆘|🚨|🔴')])
            m2.metric("Total Safety Risks", safety_count)
            m3.metric("Education Gaps 📘", len(df[df['Risk Level'].str.contains('📘')]))
            m4.metric("Retention Risks ⚠️", len(df[df['Risk Level'].str.contains('⚠️')]))

            # --- VISUAL HEATMAP ---
            st.divider()
            st.subheader("🔥 Risk Distribution Analysis")
            risk_counts = df['Risk Level'].value_counts()
            st.bar_chart(risk_counts, color="#FF4B4B")
            
            # --- DATA LOG ---
            st.subheader("📋 Executive Priority Log")
            # This sorts the highest risks to the top
            priority_df = df.sort_values(by='Risk Level', ascending=True) 
            st.dataframe(priority_df, use_container_width=True)
            
            # --- DOWNLOAD ---
            st.divider()
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📩 Download Executive Audit Report (.CSV)",
                data=csv,
                file_name='Global_Risk_Audit_2026.csv',
                mime='text/csv'
            )
        else:
            st.error("Error: Column 'review' not found in your file.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
