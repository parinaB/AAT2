import sys
import os

# Force Python looking in current folder for local scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import time
import copy
from sorting import merge_sort
from triage import PROBLEM_MAP, get_problem_details

# Page Configurations
st.set_page_config(page_title="LifeLine Tracker", page_icon="🩺", layout="centered")

# Custom UI CSS 
st.html("""
    <style>
    .main { background-color: #FAF9F6; }
    .stButton>button { background-color: #111827; color: white; border-radius: 12px; font-weight: 600; padding: 10px 24px; }
    </style>
""")

st.caption("CITY GENERAL HOSPITAL • CLINICAL DESK")
st.title("LifeLine™ Smart Triage Kiosk")
st.markdown("---")

# Session State Database Loader
if "patient_database" not in st.session_state:
    st.session_state.patient_database = [
        {"id": "P01", "name": "Aman Verma", "age": 24, "gender": "Male", "symptom": "Routine Blood Pressure Checkup", "base_priority": 5, "current_priority": 5, "total_treatment_time": 3, "remaining_time": 3, "arrival_time": 0, "waiting_in_lobby": 0},
        {"id": "P02", "name": "Priyanka Sharma", "age": 68, "gender": "Female", "symptom": "Cardiac Arrest / Heart Attack", "base_priority": 1, "current_priority": 1, "total_treatment_time": 8, "remaining_time": 8, "arrival_time": 0, "waiting_in_lobby": 0},
        {"id": "P03", "name": "Baby Kabir", "age": 3, "gender": "Male", "symptom": "High Fever with Chills & Vomiting", "base_priority": 2, "current_priority": 2, "total_treatment_time": 5, "remaining_time": 5, "arrival_time": 0, "waiting_in_lobby": 0}
    ]

# --- USER REGISTRATION FORM ---
st.subheader("👤 New Patient Intake")
with st.container(border=True):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: name = st.text_input("Name", placeholder="e.g., Rajesh")
    with col2: age = st.number_input("Age", min_value=1, max_value=110, value=25)
    with col3: sex = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    selected_complaint = st.selectbox("Select presenting clinical problem:", list(PROBLEM_MAP.keys()))
    
    EXPLAINER_MATRIX = {
        "Cardiac Arrest / Heart Attack": "🚨 **CRITICAL (Level 1):** Patient handles a suspected blockage/heart fail condition. Vitals mapping simulated severe hypoxia (O2 ~ 85%) and acute tachycardia stress. Requires immediate cardiopulmonary resuscitation bed allocation.",
        "Major Road Accident / Heavy Trauma": "🚨 **CRITICAL (Level 1):** Severe physical injury causing massive external/internal hemorrhage stress. Simulated vitals profile shows high hypovolemic shock (Systolic BP crashes to 85). Doctor burst duration maxed out.",
        "Severe Asthma / Breathing Distress": "⚠️ **URGENT (Level 2):** Severe respiratory tract constriction. Oxygen saturation is dropping below normal levels (~91%). Requires fast nebulization and acute oxygen delivery loop.",
        "Deep Bone Fracture / Acute Pain": "⚠️ **MODERATE (Level 3):** Skeletal trauma with severe acute pain pathways active. Vitals display elevated heart rate and blood pressure due to extreme shock and physical distress. Requires immobilization.",
        "High Fever with Chills & Vomiting": "⚠️ **MODERATE (Level 3):** Severe viral/bacterial infection causing high internal temperature stress and baseline dehydration symptoms. Requires fast IV line drip insertion.",
        "Moderate Migraine Headache": "🟢 **STABLE (Level 4):** Severe localized neurological pain pattern, but crucial physiological organ functions and vitals are stable. Non-life-threatening category.",
        "Minor Cut / Laceration Bleeding": "🟢 **STABLE (Level 4):** Superficial soft tissue injury with localized capillary bleeding. Blood pressure and major vitals are baseline steady. Requires simple cleaning and suturing.",
        "Mild Stomach Ache / Food Infection": "🟢 **STABLE (Level 4):** Standard gastrointestinal inflammation or food poisoning symptoms. Patient requires abdominal examination but vital metrics present no shock markers.",
        "Routine Blood Pressure Checkup": "🟢 **NON-URGENT (Level 5):** Basic routine checkup or history monitoring session. Vitals simulate a standard state (120/80 mmHg). Can safely wait if traumas arrive.",
        "General Daily Consultation": "🟢 **NON-URGENT (Level 5):** Standard walk-in outpatient care request (Minor check, renewal of scripts, cold symptoms). Minimal clinical emergency rank assignment."
    }
    
    st.info(EXPLAINER_MATRIX[selected_complaint])
    
    if st.button("📥 Add Patient to Queue", use_container_width=True):
        if name.strip() == "":
            st.warning("Please type a valid name.")
        else:
            prio, duration, _ = get_problem_details(selected_complaint, age)
            next_id = f"P{len(st.session_state.patient_database) + 1:02d}"
            
            st.session_state.patient_database.append({
                "id": next_id, "name": name, "age": age, "gender": sex, "symptom": selected_complaint,
                "base_priority": prio, "current_priority": prio, "total_treatment_time": duration,
                "remaining_time": duration, "arrival_time": 0, "waiting_in_lobby": 0
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
            st.caption(f"Complaint: {p['symptom']} • Treatment Duration: {p['total_treatment_time']} mins")
        with cr:
            if p['current_priority'] == 1: st.error("🔴 Level 1")
            elif p['current_priority'] in [2,3]: st.warning(f"🟡 Level {p['current_priority']}")
            else: st.success(f"🟢 Level {p['current_priority']}")

# --- LIVE SIMULATION MODE ---
st.markdown("---")
if st.button("🚀 Start Live Simulation Tracker", use_container_width=True):
    st.subheader("🎬 Real-Time Patient Movement Tracker")
    
    ready_queue = copy.deepcopy(st.session_state.patient_database)
    completed_patients = []
    current_patient = None
    current_time = 0
    
    live_history_logs = []
    
    clock_spot = st.empty()
    workspace_spot = st.empty()
    log_header = st.empty()
    log_spot = st.empty()
    remaining_header = st.empty()
    remaining_spot = st.empty()
    
    while ready_queue or current_patient:
        if ready_queue:
            ready_queue = merge_sort(ready_queue)
            
        # 1. CRISP ENTRY LOG (Arrow Format)
        if current_patient is None and ready_queue:
            current_patient = ready_queue.pop(0)
            entry_msg = f"⏱️ Min {current_time:02d}  |  🚪 IN   ➡️  {current_patient['name']} ({current_patient['id']})"
            live_history_logs.append(entry_msg)
            
        clock_spot.metric(label="⏳ RUNNING TIMELINE", value=f"{current_time} Mins Elapsed")
        
        if current_patient:
            current_patient['remaining_time'] -= 1
            with workspace_spot.container(border=True):
                st.markdown(f"### 🩺 Workspace: Now Treating **{current_patient['name']}**")
                st.progress(max(0, current_patient['remaining_time']) / current_patient['total_treatment_time'])
                st.caption(f"ID: {current_patient['id']} | Diagnosis: {current_patient['symptom']}")
        else:
            workspace_spot.info("Doctor is Free (Idle).")
            
        # Display Live Action Feed 
        log_header.markdown("#### 📢 Dynamic ER Movement Timeline:")
        with log_spot.container():
            st.code("\n".join(live_history_logs), language="text")
            
        # Update Pipeline status (Kaun baaki hai)
        if ready_queue:
            remaining_header.markdown("#### ⏳ Patients Remaining in Lobby:")
            rem_items = []
            for rp in ready_queue:
                rem_items.append(f"• {rp['id']} : {rp['name']} (Treatment needed: {rp['total_treatment_time']}m)")
            remaining_spot.markdown("\n".join(rem_items))
        else:
            remaining_header.empty()
            remaining_spot.empty()
            
        current_time += 1
        time.sleep(0.8) # Paced timing
        
        # 2. CRISP EXIT LOG (Arrow Format with Wait Time)
        if current_patient and current_patient['remaining_time'] == 0:
            turnaround = current_time - current_patient['arrival_time']
            wait_time = max(0, turnaround - current_patient['total_treatment_time'])
            current_patient['waiting_time'] = wait_time
            current_patient['turnaround_time'] = turnaround
            completed_patients.append(current_patient)
            
            exit_msg = f"⏱️ Min {current_time:02d}  |  🚷 OUT  ➡️  {current_patient['name']} ({current_patient['id']}) [Lobby Wait: {wait_time}m]"
            live_history_logs.append(exit_msg)
            current_patient = None
            
    # --- FINAL REPORT ---
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
   