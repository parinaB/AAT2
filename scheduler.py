import copy
from config import AGING_THRESHOLD, AGING_BONUS
from sorting import merge_sort

def run_priority_simulation(initial_batch, dynamic_arrivals):
    print("\n" + "="*60)
    print(" 🚨 EMERGENCY ROOM DOCTOR SCHEDULER INITIALIZED 🚨")
    print("="*60)
    
    current_time = 0
    ready_queue = copy.deepcopy(initial_batch)
    arrival_pool = copy.deepcopy(dynamic_arrivals)
    completed_patients = []
    gantt_chart = []
    
    current_patient = None
    
    # Run loop until all queues are completely empty and current processing terminates
    while ready_queue or arrival_pool or current_patient:
        
        # 1. Manage Dynamic Mid-Simulation Arrivals
        for patient in list(arrival_pool):
            if patient['arrival_time'] == current_time:
                ready_queue.append(patient)
                print(f"⏰ [Min {current_time:02d}] >> DOOR ARRIVAL: {patient['name']} entered ER.")
                arrival_pool.remove(patient)
        
        # 2. Dynamic Sorting: Re-prioritize waiting line
        if ready_queue:
            ready_queue = merge_sort(ready_queue)
            
        # 3. Doctor Allocation (Context Switch)
        if current_patient is None and ready_queue:
            current_patient = ready_queue.pop(0)
            print(f"🩺 [Min {current_time:02d}] >> Doctor treating: {current_patient['name']} (Priority {current_patient['current_priority']})")
            
        # 4. Process Tick
        if current_patient:
            gantt_chart.append(current_patient['id'])
            current_patient['remaining_time'] -= 1
        else:
            gantt_chart.append("IDLE")
            
        current_time += 1
        
        # 5. Aging Mechanism Implementation (Prevents Process Starvation)
        for patient in ready_queue:
            patient['waiting_in_lobby'] += 1
            if patient['waiting_in_lobby'] >= AGING_THRESHOLD:
                old_prio = patient['current_priority']
                patient['current_priority'] = max(1, patient['current_priority'] - AGING_BONUS)
                patient['waiting_in_lobby'] = 0  # reset clock cycle
                if old_prio != patient['current_priority']:
                    print(f"⚡ [AGING] {patient['name']} bumped up to Priority {patient['current_priority']} due to wait time.")
                    
        # 6. Treatment Completion Evaluation
        if current_patient and current_patient['remaining_time'] == 0:
            turnaround = current_time - current_patient['arrival_time']
            wait_time = turnaround - current_patient['total_treatment_time']
            
            current_patient['turnaround_time'] = turnaround
            current_patient['waiting_time'] = max(0, wait_time)
            
            completed_patients.append(current_patient)
            print(f"✅ [Min {current_time:02d}] >> Discharged: {current_patient['name']}. Total Wait: {current_patient['waiting_time']}m")
            current_patient = None

    _display_metrics(completed_patients, gantt_chart)


def _display_metrics(completed, gantt):
    print("\n" + "-"*18 + " SIMULATION OUTPUT METRICS " + "-"*18)
    print(f"{'ID':<6}{'Name':<15}{'Base Prio':<12}{'Wait Time':<12}{'Turnaround':<12}")
    
    total_wait = 0
    total_tat = 0
    for p in completed:
        print(f"{p['id']:<6}{p['name']:<15}{p['base_priority']:<12}{p['waiting_time']:<12}{p['turnaround_time']:<12}")
        total_wait += p['waiting_time']
        total_tat += p['turnaround_time']
        
    n = len(completed)
    print("-" * 57)
    print(f"Average Waiting Time    : {total_wait / n:.2f} minutes")
    print(f"Average Turnaround Time : {total_tat / n:.2f} minutes")
    print("\n📊 GANTT CHART REPRESENTATION:")
    print(" -> ".join(gantt))
    print("="*60)