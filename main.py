import sys
import os
import time
import copy

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sorting import merge_sort, selection_sort
from scheduler import run_priority_simulation
from triage import PROBLEM_MAP, get_problem_details

# Core list of standard problems extracted to indexed array
PROBLEMS_LIST = list(PROBLEM_MAP.keys())

patients_db = [
    {"id": "P01", "name": "Aman Verma", "age": 24, "gender": "Male", "symptom": "Routine Blood Pressure Checkup", "base_priority": 5, "current_priority": 5, "total_treatment_time": 3, "remaining_time": 3, "arrival_time": 0, "waiting_in_lobby": 0},
    {"id": "P02", "name": "Priyanka Sharma", "age": 68, "gender": "Female", "symptom": "Cardiac Arrest / Heart Attack", "base_priority": 1, "current_priority": 1, "total_treatment_time": 8, "remaining_time": 8, "arrival_time": 0, "waiting_in_lobby": 0},
    {"id": "P03", "name": "Baby Kabir", "age": 3, "gender": "Male", "symptom": "High Fever with Chills & Vomiting", "base_priority": 2, "current_priority": 2, "total_treatment_time": 5, "remaining_time": 5, "arrival_time": 0, "waiting_in_lobby": 0}
]

def display_menu():
    print("\n" + "="*50)
    print("      🩺 LIFELINE FIXED-MATRIX ER MENU 🩺      ")
    print("="*50)
    print(" [1] 📋 View Current ER Queue List")
    print(" [2] ➕ Register New Patient (From 10 Master Problems)")
    print(" [3] ⏱️  Compare Sorting Algorithms (DAA Performance)")
    print(" [4] 🚀 Execute Live Doctor Scheduler Loop (OS Process)")
    print(" [5] ❌ Close Application")
    print("="*50)

def run_interactive_terminal():
    global patients_db
    while True:
        display_menu()
        choice = input("\n👉 Enter Selection (1-5): ").strip()

        if choice == '1':
            os.system('clear' if os.name != 'nt' else 'cls')
            print("\n📋 ACTIVE WAITING LOBBY REGISTRY:")
            print("-" * 85)
            print(f"{'ID':<5}{'Patient Name':<18}{'Age/Sex':<10}{'Chief Complaint Description':<36}{'Priority':<12}")
            print("-" * 85)
            for p in patients_db:
                tag = "🔴 Critical" if p['base_priority'] == 1 else ("🟡 Urgent" if p['base_priority'] in [2,3] else "🟢 Stable")
                print(f"{p['id']:<5}{p['name']:<18}{f'{p['age']}/{p['gender'][0]}':<10}{p['symptom']:<36}{tag:<12}")
            input("\nPress Enter to return to menu...")

        elif choice == '2':
            os.system('clear' if os.name != 'nt' else 'cls')
            print("\n➕ INTAKE NEW REGISTRATION:")
            name = input("👤 Full Name: ").strip()
            if not name: continue
            
            try:
                age = int(input("🔢 Age: "))
                gender = input("🚻 Gender (M/F/Other): ").strip()
            except ValueError: continue
            
            print("\n📋 SELECT PATIENT COMPLAINT FROM MASTER 10 ER PROBLEMS:")
            for idx, prob in enumerate(PROBLEMS_LIST, 1):
                print(f"  {idx:02d}. {prob}")
                
            try:
                prob_idx = int(input("\n👉 Choice Number (1-10): ")) - 1
                if prob_idx < 0 or prob_idx >= 10: raise ValueError
            except ValueError:
                print("❌ Invalid Choice number!")
                continue

            selected_symptom = PROBLEMS_LIST[prob_idx]
            
            # Map parameters matching strict matrix rules automatically
            prio, duration, _ = get_problem_details(selected_symptom, age)
            next_id = f"P{len(patients_db) + 1:02d}"

            new_patient = {
                "id": next_id, "name": name, "age": age, "gender": gender, "symptom": selected_symptom,
                "base_priority": prio, "current_priority": prio, "total_treatment_time": duration,
                "remaining_time": duration, "arrival_time": 0, "waiting_in_lobby": 0
            }
            patients_db.append(new_patient)
            print(f"\n✅ Success! Auto-Triaged to Level {prio} based on List Choice matrix configuration.")
            input("\nPress Enter to return...")

        elif choice == '3':
            start = time.perf_counter()
            _ = selection_sort(patients_db)
            s_t = (time.perf_counter() - start) * 1000
            
            start = time.perf_counter()
            _ = merge_sort(patients_db)
            mrg_t = (time.perf_counter() - start) * 1000
            print(f"\n⏱️  Selection Sort Speed: {s_t:.4f} ms (O(n²))\n⏱️  Merge Sort Speed:     {mrg_t:.4f} ms (O(n log n))")

        elif choice == '4':
            os.system('clear' if os.name != 'nt' else 'cls')
            sorted_lobby = merge_sort(patients_db)
            run_priority_simulation(sorted_lobby[:4], sorted_lobby[4:])
            input("\nSimulation Cycle Finished. Press Enter...")

        elif choice == '5': break

if __name__ == "__main__":
    run_interactive_terminal()