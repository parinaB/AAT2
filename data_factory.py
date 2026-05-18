from triage import calculate_triage_score, estimate_treatment_time

def get_sample_dataset():
    """Returns a fresh baseline dataset of 15 patients."""
    raw_records = [
        {"id": "P01", "name": "John Doe", "hr": 72, "bp": 120, "o2": 98},
        {"id": "P02", "name": "Jane Smith", "hr": 135, "bp": 190, "o2": 88},
        {"id": "P03", "name": "Bob Johnson", "hr": 55, "bp": 140, "o2": 94},
        {"id": "P04", "name": "Alice Williams", "hr": 48, "bp": 85, "o2": 91},
        {"id": "P05", "name": "Charlie Brown", "hr": 80, "bp": 115, "o2": 99},
        {"id": "P06", "name": "Diana Prince", "hr": 110, "bp": 150, "o2": 93},
        {"id": "P07", "name": "Evan Wright", "hr": 140, "bp": 95, "o2": 87},
        {"id": "P08", "name": "Fiona Gallagher", "hr": 75, "bp": 122, "o2": 97},
        {"id": "P09", "name": "George Costanza", "hr": 95, "bp": 175, "o2": 95},
        {"id": "P10", "name": "Hannah Baker", "hr": 62, "bp": 110, "o2": 96},
        {"id": "P11", "name": "Ian Malcolm", "hr": 125, "bp": 185, "o2": 89},
        {"id": "P12", "name": "Julia Roberts", "hr": 70, "bp": 118, "o2": 98},
        {"id": "P13", "name": "Kevin Bacon", "hr": 88, "bp": 130, "o2": 94},
        {"id": "P14", "name": "Laura Croft", "hr": 115, "bp": 145, "o2": 92},
        {"id": "P15", "name": "Clark Kent", "hr": 45, "bp": 80, "o2": 86}
    ]
    
    processed_patients = []
    for record in raw_records:
        priority = calculate_triage_score(record['hr'], record['bp'], record['o2'])
        duration = estimate_treatment_time(priority)
        
        processed_patients.append({
            "id": record['id'],
            "name": record['name'],
            "base_priority": priority,
            "current_priority": priority,
            "total_treatment_time": duration,
            "remaining_time": duration,
            "arrival_time": 0,
            "waiting_in_lobby": 0
        })
        
    return processed_patients