def calculate_triage_score(heart_rate, bp, oxygen):
    """
    Translates raw vitals into an emergency priority score from 1 (Critical) to 5 (Non-Urgent).
    """
    score = 5  # Start as a standard routine patient
    
    # 1. Evaluate Oxygen saturation drops
    if oxygen < 90:
        score -= 3
    elif oxygen < 95:
        score -= 1
        
    # 2. Evaluate abnormal Heart Rate
    if heart_rate > 120 or heart_rate < 50:
        score -= 1
        
    # 3. Evaluate abnormal Blood Pressure
    if bp > 180 or bp < 90:
        score -= 1
        
    # Safe guard bounds to keep scores within real-world ESI levels (1 to 5)
    return max(1, score)


def estimate_treatment_time(priority_score):
    """
    Determines Doctor Burst Time (in minutes) based on triage intensity.
    """
    if priority_score == 1: return 8
    if priority_score == 2: return 6
    if priority_score == 3: return 5
    return 3