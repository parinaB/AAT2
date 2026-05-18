import copy
from config import AGING_THRESHOLD, AGING_BONUS

def run_priority_simulation(initial_batch, dynamic_arrivals):
    """
    OS Engine: Multilevel Queue (MLQ) Simulation with Priority & Round Robin.
    """
    from sorting import merge_sort, selection_sort  # Local imports to bypass dependency cycles
    
    print("\n" + "="*70)
    print(" 🚨 EMERGENCY ROOM LIVE SCHEDULER MONITOR ACTIVE (MLQ + RR) 🚨")
    print("="*70)
    
    current_time = 0
    master_pool = copy.deepcopy(initial_batch)
    arrival_pool = copy.deepcopy(dynamic_arrivals)
    completed_patients = []
    gantt_chart = []
    
    current_patient = None
    TIME_QUANTUM = 2  # OS Round Robin Slice Limit
    
    while master_pool or arrival_pool or current_patient:
        
        # 1. Manage Staggered Dynamic Door Traffic Mid-Simulation
        for patient in list(arrival_pool):
            if patient['arrival_time'] == current_time:
                master_pool.append(patient)
                print(f"⏰ [Min {current_time:02d}] >> EMERGENCY DOOR ARRIVAL: {patient['name']} ({patient['age']}y/{patient['gender']}) entered.")
                arrival_pool.remove(patient)
        
        # Split into Multilevel Ready Queues
        high_queue = [p for p in master_pool if p['current_priority'] <= 2]
        low_queue = [p for p in master_pool if p['current_priority'] > 2]
        
        # Sort both queues based on sorting threshold
        SORT_THRESHOLD = 10
        if high_queue:
            high_queue = merge_sort(high_queue) if len(high_queue) > SORT_THRESHOLD else selection_sort(high_queue)
        if low_queue:
            low_queue = merge_sort(low_queue) if len(low_queue) > SORT_THRESHOLD else selection_sort(low_queue)
            
        # 2. Dynamic DAA Re-sorting Step & Line Logger
        if master_pool:
            print(f"📋 [Min {current_time:02d}] Ready Queues Line ({len(high_queue)} High | {len(low_queue)} Low):")
            for p in high_queue:
                print(f"   ↳ [HIGH] {p['id']} : {p['name']} | Priority: {p['current_priority']} | Rem Burst: {p['remaining_time']}m")
            for p in low_queue:
                print(f"   ↳ [LOW]  {p['id']} : {p['name']} | Priority: {p['current_priority']} | Rem Burst: {p['remaining_time']}m")
            print("-" * 50)

        # 3. Round Robin Time Slice Preemption Check (Only for Low Queue Tasks)
        if current_patient and current_patient['current_priority'] > 2:
            if current_patient['time_slice_spent'] >= TIME_QUANTUM and current_patient['remaining_time'] > 0:
                print(f"🔄 [Min {current_time:02d}] [CONTEXT SWITCH] Quantum Expired ➡️ Moving {current_patient['name']} ({current_patient['id']}) back to queue.")
                current_patient['time_slice_spent'] = 0
                master_pool.append(current_patient)
                current_patient = None

        # 4. CPU / Doctor Allocation Engine
        if current_patient is None:
            if high_queue:
                current_patient = high_queue.pop(0)
                master_pool.remove(current_patient)
                current_patient['time_slice_spent'] = 0
                print(f"🩺 [Min {current_time:02d}] >> Doctor taking High-Priority Process: {current_patient['name']}")
            elif low_queue:
                current_patient = low_queue.pop(0)
                master_pool.remove(current_patient)
                current_patient['time_slice_spent'] = 0
                print(f"🩺 [Min {current_time:02d}] >> Doctor taking Time-Sliced Process: {current_patient['name']}")
            
        # 5. Timeline Tick Down
        if current_patient:
            gantt_chart.append(current_patient['id'])
            current_patient['remaining_time'] -= 1
            current_patient['time_slice_spent'] += 1
        else:
            gantt_chart.append("IDLE")
            
        current_time += 1
        
        # 6. Aging Logic Loop (Prevents Starvation of Stable Cases)
        for patient in master_pool:
            patient['waiting_in_lobby'] += 1
            if patient['waiting_in_lobby'] >= AGING_THRESHOLD:
                old_prio = patient['current_priority']
                patient['current_priority'] = max(1, patient['current_priority'] - AGING_BONUS)
                patient['waiting_in_lobby'] = 0
                if old_prio != patient['current_priority']:
                    print(f"⚡ [AGING IN EFFECT] {patient['name']} priority bumped up to Level {patient['current_priority']} due to long wait.")
                    
        # 7. Discharge Evaluation on Process Completion
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
        age_sex = f"{p['age']}/{p['gender'][0]}" 
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