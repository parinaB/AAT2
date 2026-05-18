import sys
import os
import time
import copy

# Force Python to look in the current folder for local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_factory import get_sample_dataset
from sorting import merge_sort, selection_sort
from scheduler import run_priority_simulation
from triage import calculate_triage_score, estimate_treatment_time

def clear_screen():
    # Terminal ko saaf rakhne ke liye helper
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n" + "="*45)
    print("      🩺 LIFELINE EMERGENCY ROOM MENU 🩺      ")
    print("="*45)
    print(" [1] 📋 View Current Patient Waiting List")
    print(" [2] ➕ Add New Emergency Patient")
    print(" [3] ⏱️  Run DAA Sorting Benchmark Performance")
    print(" [4] 🚀 Start OS Doctor Allocation Simulation")
    print(" [5] ❌ Exit Application")
    print("="*45)

def run_interactive_terminal():
    # Load 15 standard patients from factory as starting database
    patients_db = get_sample_dataset()
    
    # Custom adjustments: Filter or keep a clean pool
    # Truncating to 7 as per your previous preference, feel free to add more!
    patients_db = patients_db[:7]

    while True:
        display_menu()
        choice = input("\n👉 Enter your choice (1-5): ").strip()

        if choice == '1':
            clear_screen()
            print("\n📋 CURRENT PATIENT WAITING LIST IN LOBBY:")
            print("-" * 65)
            print(f"{'ID':<6}{'Patient Name':<20}{'Base Priority':<15}{'Treatment Time':<15}")
            print("-" * 65)
            for p in patients_db:
                # Priority text mapping for terminal readability
                prio_txt = "🔴 Critical" if p['base_priority'] == 1 else ("🟡 Urgent" if p['base_priority'] in [2,3] else "🟢 Stable")
                print(f"{p['id']:<6}{p['name']:<20}{prio_txt:<15}{p['total_treatment_time']:<2} mins")
            print("-" * 65)
            input("\nPress Enter to return to Menu...")

        elif choice == '2':
            clear_screen()
            print("\n➕ REGISTER NEW INCOMING PATIENT:")
            print("-" * 40)
            name = input("👤 Enter Patient Full Name: ").strip()
            if not name:
                print("❌ Error: Name cannot be blank!")
                time.sleep(1.5)
                continue
            
            print("\nSelect Main Complaint Severity:")
            print(" 1. Severe Chest Pain / Heavy Bleeding (Critical)")
            print(" 2. Mild Fever / Persistent Cough (Moderate)")
            print(" 3. Routine Body Checkup (Stable)")
            comp_choice = input("Select Option (1-3): ").strip()

            # Set parameters based on selection
            if comp_choice == '1':
                o2, hr, bp = 88, 130, 185
            elif comp_choice == '2':
                o2, hr, bp = 94, 95, 135
            else:
                o2, hr, bp = 98, 75, 120

            prio = calculate_triage_score(hr, bp, o2)
            duration = estimate_treatment_time(prio)
            next_id = f"P{len(patients_db) + 1:02d}"

            new_patient = {
                "id": next_id, "name": name, "base_priority": prio, "current_priority": prio,
                "total_treatment_time": duration, "remaining_time": duration, "arrival_time": 0, "waiting_in_lobby": 0
            }
            patients_db.append(new_patient)
            print(f"\n✅ Success: {name} registered as ID {next_id} with Priority Level {prio}!")
            input("\nPress Enter to return to Menu...")

        elif choice == '3':
            clear_screen()
            print("\n⏱️  RUNNING DAA TRIAGE SORTING BENCHMARK...")
            print("-" * 50)
            
            start = time.perf_counter()
            _ = selection_sort(patients_db)
            sel_time = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            _ = merge_sort(patients_db)
            mrg_time = (time.perf_counter() - start) * 1000

            print(f"🔹 Selection Sort Time : {sel_time:.4f} ms | Complexity: O(n²)")
            print(f"🔹 Merge Sort Time     : {mrg_time:.4f} ms | Complexity: O(n log n)")
            print("-" * 50)
            print("💡 Observation: Merge Sort splits processing load exponentially, making it ideal for massive ER queues!")
            input("\nPress Enter to return to Menu...")

        elif choice == '4':
            clear_screen()
            print("\n🚀 BOOTING CPU PARTITION SCHEDULER...")
            time.sleep(1)
            
            # Use Merge Sort to arrange current lobby list by priority before running simulation
            sorted_lobby = merge_sort(patients_db)
            
            # Separate them into initial batch and dynamic mid-sim arrivals
            # First 5 are inside, next ones arrive dynamically at staggered times
            initial_batch = sorted_lobby[:5]
            dynamic_arrivals = sorted_lobby[5:]
            
            for idx, p in enumerate(dynamic_arrivals):
                p['arrival_time'] = (idx + 1) * 6  # Arrives at min 6, 12, etc.

            # Hand off data to our simulation runner inside scheduler.py
            run_priority_simulation(initial_batch, dynamic_arrivals)
            input("\nSimulation Complete. Press Enter to return to Menu...")

        elif choice == '5':
            clear_screen()
            print("\n👋 Shutting down LifeLine Triage Engine. Take care, Doc!")
            break
        else:
            print("❌ Invalid input! Please enter a number between 1 and 5.")
            time.sleep(1.5)

if __name__ == "__main__":
    run_interactive_terminal()