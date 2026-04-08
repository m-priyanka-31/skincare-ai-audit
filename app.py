def analyze_review(text):
    text = str(text).lower()
    
    # 1. EMERGENCY (Safety/Legal)
    emergency = [
        'doctor', 'hospital', 'emergency', 'pain', 'allergic reaction',
        'emergencia', 'dolor', 'reacción alérgica'
    ]
    
    # 2. MEDICAL (Symptoms)
    medical = [
        'burn', 'red', 'puffy', 'rash', 'swollen', 'break out', 
        'stings', 'irritation', 'irritate', 'allergy',
        'quemadura', 'rojo', 'hinchado', 'irritación', 'alergia'
    ]
    
    # 3. EDUCATION (Usage Confusion)
    # This catches customers who don't know how to use the product
    education = [
        'how to', 'confused', 'order', 'step', 'every day', 'shake',
        'como usar', 'confundido', 'paso' # Spanish: "How to use", "Confused", "Step"
    ]
    
    # 4. QUALITY (Product/Packaging)
    quality = [
        'broken', 'leaked', 'empty', 'smell', 'texture', 'harsh', 'amount',
        'roto', 'vacío', 'olor', 'textura', 'cantidad'
    ]

    # THE LOGIC HIERARCHY
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
