# Master Map linking problems directly to clinical parameters
PROBLEM_MAP = {
    "Cardiac Arrest / Heart Attack":             {"prio": 1, "time": 8, "vitals": (85, 140, 190)},
    "Major Road Accident / Heavy Trauma":        {"prio": 1, "time": 8, "vitals": (88, 130, 85)},
    "Severe Asthma / Breathing Distress":        {"prio": 2, "time": 6, "vitals": (91, 115, 140)},
    "Deep Bone Fracture / Acute Pain":           {"prio": 3, "time": 5, "vitals": (96, 105, 150)},
    "High Fever with Chills & Vomiting":         {"prio": 3, "time": 5, "vitals": (95, 110, 130)},
    "Moderate Migraine Headache":                {"prio": 4, "time": 3, "vitals": (98, 85, 135)},
    "Minor Cut / Laceration Bleeding":           {"prio": 4, "time": 3, "vitals": (99, 80, 125)},
    "Mild Stomach Ache / Food Infection":        {"prio": 4, "time": 3, "vitals": (97, 78, 118)},
    "Routine Blood Pressure Checkup":            {"prio": 5, "time": 3, "vitals": (98, 72, 120)},
    "General Daily Consultation":                {"prio": 5, "time": 3, "vitals": (99, 70, 115)}
}

def get_problem_details(symptom_name, age=30):
    """
    Looks up the master database to return exact Priority, 
    Treatment Duration, and Vitals. Applies Age Bias dynamically.
    """
    if symptom_name not in PROBLEM_MAP:
        # Fallback security profile
        return 5, 3, (98, 72, 120)
        
    data = PROBLEM_MAP[symptom_name]
    final_prio = data["prio"]
    
    # Age Bias: Pediatric (<5) and Geriatric (>65) get priority bump for moderate issues
    if (age <= 5 or age >= 65) and final_prio > 1:
        final_prio = max(1, final_prio - 1)
        
    return final_prio, data["time"], data["vitals"]