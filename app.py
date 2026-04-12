import streamlit as st
import pandas as pd
import re

# --- THE UPDATED RISK ENGINE ---
def analyze_review(text):
    # Ensure text is a string and lowercase for consistent matching
    text_clean = str(text).lower()
    
    # 0. THE CONTEXTUAL MASK (Keywords that trick standard AI)
    masking_keywords = ['glow', 'glowing', 'radiant','radiante', 'luminosa','shimmer', 'bright', 'glass skin', 'radiance']
    
    # 1. EMERGENCY (Safety/Legal) - Global Lexicon
    emergency = [
        'doctor', 'hospital', 'emergency', 'pain', 'allergic reaction',
        'emergencia', 'dolor', 'reacción alérgica',
        'medico', 'ospedale', 'pronto soccorso', 'reazione allergica'
    ]
    
    # 2. MEDICAL (Symptoms) - Global Lexicon
    # Added 'hot' and 'itchy' specifically to fix the logic leak
    medical = [
        'burn', 'red', 'puffy', 'rash', 'swollen', 'break out', 'hot', 'itchy',
        'stings', 'irritation', 'irritate', 'allergy', 'peeling', 'blisters',
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

    # --- BOOLEAN CHECKERS ---
    has_mask = any(mask in text_clean for mask in masking_keywords)
    has_medical = any(word in text_clean for word in medical)
    has_emergency = any(word in text_clean for word in emergency)
    has_education = any(word in text_clean for word in education)
    has_quality = any(word in text_clean for word in quality)

    # --- HIERARCHICAL LOGIC (Priority Order) ---
    
    # Priority 1: Direct Emergency/Legal Risk
    if has_emergency: 
        return "🆘 EMERGENCY: High Legal Risk"
    
    # Priority 2: THE FIX - Masked Adverse Reaction (Glow + Symptom)
    elif has_mask and has_medical:
        return "🔴 CRITICAL: Masked Adverse Reaction"
        
    # Priority 3: Direct Medical Signal
    elif has_medical: 
        return "🚨 MEDICAL: Adverse Reaction"
    
    # Priority 4: Education Gaps
    elif has_education: 
        return "📘 EDUCATION: Usage Confusion"
    
    # Priority 5: Quality/Retention Issues
    elif has_quality:
        return "⚠️ QUALITY: Retention Risk"
    
    # Priority 6: Standard Feedback
    else: 
        return "✅ ROUTINE: Brand Engagement"

# --- STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Skincare Risk Audit Pro", layout="wide", page_icon="🧪")

st.title("🧪 Skincare Risk Audit: Enterprise Edition")
st.markdown("### Automated Safety & Global Compliance Monitoring")
st.divider()

# --- SIDEBAR: REAL-TIME TESTING ---
st.sidebar.header("🔬 Sandbox Testing")
st.sidebar.write("Test specific phrases for 'The Glowing Bias' here.")
single_input = st.sidebar.text_area("Review Text:", placeholder="e.g., My face is glowing but it feels hot and itchy.")

if st.sidebar.button("Analyze Logic"):
    if single_input:
        result = analyze_review(single_input)
        if "🔴" in result or "🆘" in result:
            st.sidebar.error(f"Analysis: {result}")
        elif "🚨" in result:
            st.sidebar.warning(f"Analysis: {result}")
        else:
            st.sidebar.success(f"Analysis: {result}")

# --- MAIN: BULK AUDIT ---
st.header("📊 Bulk Brand Audit")
uploaded_file = st.file_uploader("Upload CSV or Excel for batch processing", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if 'review' in df.columns:
            # Apply the engine
            df['Audit Result'] = df['review'].apply(analyze_review)
            
            # --- DASHBOARD METRICS ---
            st.subheader("Executive Overview")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Reviews", len(df))
            
            critical_count = len(df[df['Audit Result'].str.contains('🆘|🔴|🚨')])
            m2.metric("Safety/Legal Risks", critical_count, delta_color="inverse")
            
            edu_count = len(df[df['Audit Result'].str.contains('📘')])
            m3.metric("Education Gaps", edu_count)
            
            quality_count = len(df[df['Audit Result'].str.contains('⚠️')])
            m4.metric("Quality Flags", quality_count)

            # --- VISUALIZATION ---
            st.divider()
            col_chart, col_data = st.columns([1, 2])
            
            with col_chart:
                st.write("### Risk Distribution")
                counts = df['Audit Result'].value_counts()
                st.bar_chart(counts, color="#FF4B4B")

            with col_data:
                st.write("### Priority Log")
                # Showing high risks first
                st.dataframe(df.sort_values(by='Audit Result'), use_container_width=True)
            
            # --- EXPORT ---
            st.divider()
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Executive Audit Report",
                data=csv,
                file_name='Global_Risk_Audit_Report.csv',
                mime='text/csv'
            )
        else:
            st.error("CSV must contain a column named 'review'.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
