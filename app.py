import csv
import json

# =====================================================================
# DETERMINISTIC CLINICAL LEXICON (TIERED BY SEVERITY)
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
    "marks", "hyperpigmentation", "dark spots"
]

# High-frequency praise terms that typically skew standard NLP tools
PRAISE_KEYWORDS = ["glow", "effective", "good", "nice", "love", "radiant", "awesome", "best"]

# =====================================================================
# CORE HIERARCHICAL RISK ENGINE LOGIC
# =====================================================================

def analyze_review_safety(review_text, rating):
    """
    Parses a review string using a deterministic hierarchical priority override.
    Detects if marketing praise is masking an underlying physiological safety risk.
    """
    text_lower = review_text.lower()
    
    # 1. Execute Hierarchical Keyword Search (Highest Severity First)
    triggered_flag = None
    assigned_risk = "LOW"
    
    for word in TIER_1_CRITICAL:
        if word in text_lower:
            assigned_risk = "CRITICAL"
            triggered_flag = word
            break  # Strict override: exit loop early once highest severity is hit
            
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

    # 2. Identify "Masked Risk" Gaps (The Glow Bias)
    # Occurs when a safety risk is detected alongside a high star rating or praise keywords
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
# BATCH PROCESSING PIPELINE
# =====================================================================

def run_risk_gap_analysis(input_csv_path, output_json_path):
    """
    Reads unedited product reviews from a CSV file, processes them through
    the override architecture, and exports a structured validation report.
    """
    metrics = {
        "total_processed": 0,
        "critical_flags": 0,
        "high_flags": 0,
        "medium_flags": 0,
        "low_flags": 0,
        "total_masked_risks_hidden": 0
    }
    
    detailed_results = []

    try:
        with open(input_csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Verify required columns exist in the source CSV
            if 'review_text' not in reader.fieldnames or 'rating' not in reader.fieldnames:
                print("Error: CSV must contain 'review_text' and 'rating' columns.")
                return

            for row in reader:
                metrics["total_processed"] += 1
                analysis = analyze_review_safety(row['review_text'], row['rating'])
                
                # Update aggregate metrics
                if analysis["risk_level"] == "CRITICAL": metrics["critical_flags"] += 1
                elif analysis["risk_level"] == "HIGH": metrics["high_flags"] += 1
                elif analysis["risk_level"] == "MEDIUM": metrics["medium_flags"] += 1
                else: metrics["low_flags"] += 1
                
                if analysis["masked_risk_detected"]:
                    metrics["total_masked_risks_hidden"] += 1

                # Append detailed breakdown for reporting
                detailed_results.append({
                    "raw_text": row['review_text'],
                    "analysis": analysis
                })

        # Calculate exact percentage gap for the brand report
        if metrics["total_processed"] > 0:
            metrics["masked_risk_percentage_gap"] = round(
                (metrics["total_masked_risks_hidden"] / metrics["total_processed"]) * 100, 2
            )
        else:
            metrics["masked_risk_percentage_gap"] = 0.0

        # Compile and export final data packet
        output_data = {
            "summary_metrics": metrics,
            "processed_records": detailed_results
        }

        with open(output_json_path, 'w', encoding='utf-8') as out_file:
            json.dump(output_data, out_file, indent=4)

        print(f"Analysis Complete. Processed {metrics['total_processed']} reviews.")
        print(f"Found {metrics['total_masked_risks_hidden']} masked risks ({metrics['masked_risk_percentage_gap']}% of total data).")
        print(f"Full report exported successfully to: {output_json_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found. Please check your path.")

# =====================================================================
# LOCAL EXECUTION TEST SCRIPT
# =====================================================================
if __name__ == "__main__":
    # 1. Create a quick local test CSV file to verify the engine pipeline works
    test_csv = "sample_brand_reviews.csv"
    with open(test_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["review_text", "rating"])
        writer.writerow(["This serum gave me an amazing glow! But my face is burning and raw skin is peeling off.", "5"])
        writer.writerow(["Very effective product, reduced my spots completely.", "5"])
        writer.writerow(["Nice texture, but it triggered an allergic rash and painful bumps on my jawline.", "4"])
        writer.writerow(["Did not suit my skin, caused a bad breakout.", "2"])

    # 2. Run the processing engine on the test dataset
    run_risk_gap_analysis(test_csv, "brand_risk_report.json")
