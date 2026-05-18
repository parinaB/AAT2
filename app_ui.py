import sys
import os

# Force Python looking in current folder for local scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import time
import copy
from sorting import merge_sort, selection_sort
from triage import PROBLEM_MAP, get_problem_details
from config import AGING_THRESHOLD, AGING_BONUS

# Page Configurations
st.set_page_config(page_title="LifeLine Tracker", page_icon="🩺", layout="centered")

st.html("""
    <style>
    .main { background-color: #FAF9F6; }
    .stButton>button { background-color: #111827; color: white; border-radius: 12px; font-weight: 600; padding: 10px 24px; }
    </style>
""")

st.caption("CITY GENERAL HOSPITAL • CLINICAL DESK • MULTILEVEL INTERACTIVE SCHEDULER")
st.title("LifeLine™ Smart Triage Kiosk")
st.markdown("---")

# Session State Database Loader (Sync 6-Process Starter Array)
if "patient_database" not in st.session_state:
    st.session_state.patient_database = [
        {"id": "P01", "name": "Priyanka Sharma", "age": 68, "gender": "Female", "symptom": "Cardiac Arrest / Heart Attack", "base_priority": 1, "current_priority": 1, "total_treatment_time": 5, "remaining_time": 5, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0},
        {"id": "P02", "name": "Rohan Mehra", "age": 32, "gender": "Male", "symptom": "Major Road Accident / Heavy Trauma", "base_priority": 1, "current_priority": 1, "total_treatment_time": 4, "remaining_time": 4, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0},
        {"id": "P03", "name": "Kabir", "age": 3, "gender": "Male", "symptom": "High Fever with Chills & Vomiting", "base_priority": 2, "current_priority": 2, "total_treatment_time": 3, "remaining_time": 3, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0},
        {"id": "P04", "name": "Rajesh Kumar", "age": 55, "gender": "Male", "symptom": "Deep Bone Fracture / Acute Pain", "base_priority": 3, "current_priority": 3, "total_treatment_time": 4, "remaining_time": 4, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0},
        {"id": "P05", "name": "Vikram Singh", "age": 29, "gender": "Male", "symptom": "Deep Bone Fracture / Acute Pain", "base_priority": 3, "current_priority": 3, "total_treatment_time": 3, "remaining_time": 3, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0},
        {"id": "P06", "name": "Aman Verma", "age": 24, "gender": "Male", "symptom": "Routine Blood Pressure Checkup", "base_priority": 5, "current_priority": 5, "total_treatment_time": 3, "remaining_time": 3, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0}
    ]

# --- USER REGISTRATION FORM ---
st.subheader("👤 New Patient Intake")
with st.container(border=True):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: name = st.text_input("Name", placeholder="e.g., Rajesh")
    with col2: age = st.number_input("Age", min_value=1, max_value=110, value=25)
    with col3: sex = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    selected_complaint = st.selectbox("Select presenting clinical problem:", list(PROBLEM_MAP.keys()))
    
    if st.button("📥 Add Patient to Queue", use_container_width=True):
        if name.strip() == "":
            st.warning("Please type a valid name.")
        else:
            prio, duration, _ = get_problem_details(selected_complaint, age)
            next_id = f"P{len(st.session_state.patient_database) + 1:02d}"
            
            st.session_state.patient_database.append({
                "id": next_id, "name": name, "age": age, "gender": sex, "symptom": selected_complaint,
                "base_priority": prio, "current_priority": prio, "total_treatment_time": duration,
                "remaining_time": duration, "arrival_time": 0, "waiting_in_lobby": 0, "time_slice_spent": 0
            })
            st.success(f"Added {name} successfully!")
            time.sleep(0.4)
            st.rerun()

# --- LOBBY SUMMARY VIEW ---
st.markdown("---")
st.subheader("👥 Patients Currently Waiting in Lobby")
for p in st.session_state.patient_database:
    with st.container(border=True):
        cl, cr = st.columns([3, 1])
        with cl:
            st.markdown(f"**{p['id']} | {p['name']}** ({p['age']}/{p['gender'][0]})")
            st.caption(f"Routing Profile: {'🔴 High-Priority Queue' if p['current_priority'] <= 2 else '🔵 Low-Priority (Round Robin)'}")
        with cr:
            st.info(f"Prio: {p['current_priority']}")

# --- LIVE SIMULATION MODE ---
st.markdown("---")
if st.button("🚀 Start Live Simulation Tracker", use_container_width=True):
    st.subheader("🎬 Real-Time Process Movement Tracker")
    
    master_pool = copy.deepcopy(st.session_state.patient_database)
    completed_patients = []
    current_patient = None
    current_time = 0
    live_history_logs = []
    gantt_chart_trace = []
    
    clock_spot = st.empty()
    workspace_spot = st.empty()
    gantt_header = st.empty()
    gantt_spot = st.empty()
    log_header = st.empty()
    log_spot = st.empty()
    remaining_header = st.empty()
    remaining_spot = st.empty()
    
    TIME_QUANTUM = 2  
    
    while master_pool or current_patient:
        
        # Multilevel Queue splitting
        high_prio_queue = [p for p in master_pool if p['current_priority'] <= 2]
        low_prio_queue = [p for p in master_pool if p['current_priority'] > 2]
        
        # Sort using dynamic threshold rules
        SORT_THRESHOLD = 5
        if high_prio_queue:
            high_prio_queue = merge_sort(high_prio_queue) if len(high_prio_queue) > SORT_THRESHOLD else selection_sort(high_prio_queue)
        if low_prio_queue:
            low_prio_queue = merge_sort(low_prio_queue) if len(low_prio_queue) > SORT_THRESHOLD else selection_sort(low_prio_queue)
            
        # 1. ROUND ROBIN PREEMPTION CHECK (Only for Low Priority)
        if current_patient and current_patient['current_priority'] > 2:
            if current_patient['time_slice_spent'] >= TIME_QUANTUM and current_patient['remaining_time'] > 0:
                rr_msg = f"🔄 Min {current_time:02d}  |  🤖 ALGO ➡️ TIME QUANTUM EXPIRED Context Switch: {current_patient['name']} ({current_patient['id']}) returned to low queue."
                live_history_logs.append(rr_msg)
                current_patient['time_slice_spent'] = 0
                master_pool.append(current_patient)
                current_patient = None
        
        # 2. SELECTION / INJECTION LOGIC FOR CPU TIME
        if current_patient is None:
            if high_prio_queue:
                current_patient = high_prio_queue.pop(0)
                master_pool.remove(current_patient)
                current_patient['time_slice_spent'] = 0
                live_history_logs.append(f"⏱️ Min {current_time:02d}  |  🚪 IN   ➡️ {current_patient['name']} ({current_patient['id']}) [High-Priority Ward]")
            elif low_prio_queue:
                current_patient = low_prio_queue.pop(0)
                master_pool.remove(current_patient)
                current_patient['time_slice_spent'] = 0
                live_history_logs.append(f"⏱️ Min {current_time:02d}  |  🚪 IN   ➡️ {current_patient['name']} ({current_patient['id']}) [Time-Sliced OPD Ward]")
            
        clock_spot.metric(label="⏳ RUNNING TIMELINE", value=f"{current_time} Mins Elapsed")
        
        if current_patient:
            gantt_chart_trace.append(current_patient['id'])
            current_patient['remaining_time'] -= 1
            current_patient['time_slice_spent'] += 1
            with workspace_spot.container(border=True):
                st.markdown(f"### 🩺 Workspace: Now Treating **{current_patient['name']}**")
                st.progress(max(0, current_patient['remaining_time']) / current_patient['total_treatment_time'])
                st.caption(f"ID: {current_patient['id']} | Mode: {'Priority' if current_patient['current_priority']<=2 else 'Round Robin'} | Rem Burst: {current_patient['remaining_time']}m")
        else:
            gantt_chart_trace.append("IDLE")
            workspace_spot.info("Doctor is Free (Idle).")
            
        # Update Gantt UI trace instantly
        gantt_header.markdown("#### 📊 Live CPU Gantt Chart Trace:")
        gantt_spot.code(" -> ".join(gantt_chart_trace), language="text")
        
        # Display Live Action Feed 
        log_header.markdown("#### 📢 Dynamic ER Movement Timeline:")
        with log_spot.container():
            st.code("\n".join(live_history_logs), language="text")
            
        # Display pipeline list
        if master_pool:
            remaining_header.markdown("#### ⏳ Processes Remaining in Ready Queue Loops:")
            rem_items = []
            for rp in master_pool:
                rem_items.append(f"• {rp['id']} : {rp['name']} | Priority: {rp['current_priority']} | Rem Burst: {rp['remaining_time']}m")
            remaining_spot.markdown("\n".join(rem_items))
        else:
            remaining_header.empty()
            remaining_spot.empty()
            
        current_time += 1
        time.sleep(0.6)
        
        # 3. LIVE AGING SYSTEM BUMP ENGINE
        for patient in master_pool:
            patient['waiting_in_lobby'] += 1
            if patient['waiting_in_lobby'] >= AGING_THRESHOLD:
                old_prio = patient['current_priority']
                patient['current_priority'] = max(1, patient['current_priority'] - AGING_BONUS)
                patient['waiting_in_lobby'] = 0  
                if old_prio != patient['current_priority']:
                    aging_msg = f"⏱️ Min {current_time:02d}  |  ⚡ BUMP ➡️  {patient['name']} ({patient['id']}) promoted to Level {patient['current_priority']} due to starvation wait."
                    live_history_logs.append(aging_msg)
        
        # 4. CRISP EXIT LOG ON PROCESS COMPLETION
        if current_patient and current_patient['remaining_time'] == 0:
            turnaround = current_time - current_patient['arrival_time']
            wait_time = max(0, turnaround - current_patient['total_treatment_time'])
            current_patient['waiting_time'] = wait_time
            current_patient['turnaround_time'] = turnaround
            completed_patients.append(current_patient)
            
            exit_msg = f"⏱️ Min {current_time:02d}  |  🚷 OUT  ➡️  {current_patient['name']} ({current_patient['id']}) [Lobby Wait: {wait_time}m]"
            live_history_logs.append(exit_msg)
            current_patient = None
            
    # --- FINAL REPORT SUMMARY ---
    st.markdown("---")
    st.subheader("📊 Final Discharge Performance Summary Report")
    
    summary_data = []
    for cp in completed_patients:
        summary_data.append({
            "Patient ID": cp['id'], "Patient Name": cp['name'], "Problem/Symptom": cp['symptom'],
            "Doctor Time (mins)": cp['total_treatment_time'], "Lobby Wait Time (mins)": cp['waiting_time'],
            "Total Process Time (TAT)": cp['turnaround_time']
        })
        
    df_report = pd.DataFrame(summary_data)
    st.dataframe(df_report, use_container_width=True, hide_index=True)
    
    avg_wait = df_report["Lobby Wait Time (mins)"].mean()
    avg_tat = df_report["Total Process Time (TAT)"].mean()
    
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1: st.metric("Average Waiting Time", f"{avg_wait:.2f} mins")
    with stat_col2: st.metric("Average Turnaround Time (TAT)", f"{avg_tat:.2f} mins")
    st.balloons()