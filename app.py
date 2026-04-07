import streamlit as st
import pandas as pd

# --- THE ENGINE ---
def analyze_review(text):
    text = str(text).lower()
    emergency = ['stuck', 'doctor', 'emergency', 'blind', 'scared', 'pain']
    medical = ['eczema', 'rash', 'burn', 'swollen', 'itchy', 'break out', 'redness', 'stings', 'stripped', 'irritated']
    education = ['how to', 'confused', 'order', 'step', 'every day']
    quality = ['pump', 'broken', 'leaked', 'empty', 'smell', 'texture', 'watery', 'harsh', 'dryness']

    if any(word in text for word in emergency): return "🆘 EMERGENCY"
    elif any(word in text for word in medical): return "🚨 MEDICAL"
    elif any(word in text for word in education): return "📘 EDUCATION"
    elif any(word in text for word in quality): return "⚠️ QUALITY"
    else: return "✅ ROUTINE"

# --- THE USER INTERFACE ---
st.set_page_config(page_title="Skincare Risk Audit Pro", layout="wide")
st.title("🧪 Skincare Risk Audit: Enterprise Edition")

# --- SIDEBAR: SINGLE REVIEW ---
st.sidebar.header("Single Review Audit")
single_input = st.sidebar.text_area("Paste one review:")
if st.sidebar.button("Audit Single"):
    st.sidebar.write(f"Result: **{analyze_review(single_input)}**")

# --- MAIN: BULK UPLOAD ---
st.header("Bulk Data Analysis")
st.write("Upload a CSV file of customer reviews to generate a Brand Risk Report.")

uploaded_file = st.file_uploader("Choose a CSV file (Column name should be 'review')", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if 'review' in df.columns:
        # Run the AI on every row
        df['Risk Level'] = df['review'].apply(analyze_review)
        
        # Display Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews", len(df))
        col2.metric("High Risk (Emergency/Medical)", len(df[df['Risk Level'].str.contains('🆘|🚨')]))
        col3.metric("Retention Risk (Quality)", len(df[df['Risk Level'] == '⚠️ QUALITY']))

        # Show the Data Table
        st.subheader("Audit Results")
        st.dataframe(df, use_container_width=True)
        
        # Download Button for the Brand
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Full Audit Report", csv, "brand_audit.csv", "text/csv")
    else:
        st.error("Error: Please make sure your CSV has a column named 'review'.")
