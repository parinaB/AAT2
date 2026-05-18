import copy
from config import AGING_THRESHOLD, AGING_BONUS

def run_priority_simulation(initial_batch, dynamic_arrivals):
    """
    OS Engine: Priority Scheduling Simulation with support for Age, Gender, and Custom Symptoms.
    """
    from sorting import merge_sort  # Local import to prevent circular dependencies
    
    print("\n" + "="*70)
    print(" 🚨 EMERGENCY ROOM LIVE SCHEDULER MONITOR ACTIVE 🚨")
    print("="*70)
    
    current_time = 0
    ready_queue = copy.deepcopy(initial_batch)
    arrival_pool = copy.deepcopy(dynamic_arrivals)
    completed_patients = []
    gantt_chart = []
    
    current_patient = None
    
    while ready_queue or arrival_pool or current_patient:
        
        # 1. Manage Staggered Dynamic Door Traffic Mid-Simulation
        for patient in list(arrival_pool):
            if patient['arrival_time'] == current_time:
                ready_queue.append(patient)
                print(f"⏰ [Min {current_time:02d}] >> EMERGENCY DOOR ARRIVAL: {patient['name']} ({patient['age']}y/{patient['gender']}) entered.")
                arrival_pool.remove(patient)
        
        # 2. Dynamic DAA Re-sorting Step
        if ready_queue:
            ready_queue = merge_sort(ready_queue)
            
        # 3. Doctor/CPU Allocation (Context Switch)
        if current_patient is None and ready_queue:
            current_patient = ready_queue.pop(0)
            print(f"🩺 [Min {current_time:02d}] >> Doctor taking: {current_patient['name']} | Symptom: {current_patient['symptom']}")
            
        # 4. Timeline Tick Down
        if current_patient:
            gantt_chart.append(current_patient['id'])
            current_patient['remaining_time'] -= 1
        else:
            gantt_chart.append("IDLE")
            
        current_time += 1
        
        # 5. Aging Logic Loop (Prevents Starvation of Stable Cases)
        for patient in ready_queue:
            patient['waiting_in_lobby'] += 1
            if patient['waiting_in_lobby'] >= AGING_THRESHOLD:
                old_prio = patient['current_priority']
                patient['current_priority'] = max(1, patient['current_priority'] - AGING_BONUS)
                patient['waiting_in_lobby'] = 0  # reset clock cycle
                if old_prio != patient['current_priority']:
                    print(f"⚡ [AGING IN EFFECT] {patient['name']} priority bumped up to Level {patient['current_priority']} due to long wait.")
                    
        # 6. Discharge Evaluation on Process Completion
        if current_patient and current_patient['remaining_time'] == 0:
            turnaround = current_time - current_patient['arrival_time']
            wait_time = turnaround - current_patient['total_treatment_time']
            
            current_patient['turnaround_time'] = turnaround
            current_patient['waiting_time'] = max(0, wait_time)
            
            completed_patients.append(current_patient)
            print(f"✅ [Min {current_time:02d}] >> Discharged: {current_patient['name']}. Total Lobby Wait Time: {current_patient['waiting_time']} mins.")
            current_patient = None

    _display_terminal_metrics(completed_patients, gantt_chart)


def _display_terminal_metrics(completed, gantt):
    print("\n" + "-" * 23 + " SIMULATION STATS OVERVIEW " + "-" * 23)
    print(f"{'ID':<6}{'Name':<18}{'Age/Sex':<10}{'Priority':<10}{'Wait Time':<12}{'Turnaround':<12}")
    print("-" * 68)
    
    total_wait = 0
    total_tat = 0
    for p in completed:
        age_sex = f"{p['age']}/{p['gender'][0]}" # e.g., 24/M
        print(f"{p['id']:<6}{p['name']:<18}{age_sex:<10}{p['base_priority']:<10}{p['waiting_time']:<12}{p['turnaround_time']:<12}")
        total_wait += p['waiting_time']
        total_tat += p['turnaround_time']
        
    n = len(completed)
    print("-" * 68)
    print(f"Average Waiting Time    : {total_wait / n:.2f} minutes")
    print(f"Average Turnaround Time : {total_tat / n:.2f} minutes")
    print("\n📊 HORIZONTAL GANTT CHART CHRONOLOGY (CPU TRACE):")
    print(" -> ".join(gantt))
    print("=" * 70 + "\n")