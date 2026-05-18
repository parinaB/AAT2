import sys
import os

# Force Python looking in current folder for local scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import time
import copy
from sorting import merge_sort
from triage import calculate_triage_score, estimate_treatment_time

# Page Configurations - Premium Centered Experience
st.set_page_config(page_title="LifeLine ER", page_icon="🩺", layout="centered")

# Smooth Humanized Design Tweaks (Custom clean look)
st.html("""
    <style>
    .main { background-color: #FAF9F6; } /* Premium Soft White Background */
    div[data-testid="stExpander"] { border-radius: 16px !important; border: 1px solid #E2E8F0 !important; }
    .stButton>button { background-color: #111827; color: white; border-radius: 14px; padding: 12px 24px; font-weight: 600; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #1A52EC; }
    </style>
""")

# Minimalistic App Brand Header (Athena Style Minimalism)
st.caption("CITY GENERAL HOSPITAL • EMERGENGY ROOM KIOSK")
st.title("LifeLine™ Triage Engine")
st.markdown("---")

# --- INITIAL CUSTOM DATA FACTORY ---
if "patient_database" not in st.session_state:
    raw_records = [
        {"id": "P01", "name": "Aman Verma", "hr": 72, "bp": 120, "o2": 98},
        {"id": "P02", "name": "Priyanka Sharma", "hr": 135, "bp": 190, "o2": 88},
        {"id": "P03", "name": "Rajesh Kumar", "hr": 55, "bp": 140, "o2": 94},
        {"id": "P04", "name": "Vikram Singh", "hr": 48, "bp": 85, "o2": 91}
    ]
    processed = []
    for r in raw_records:
        prio = calculate_triage_score(r['hr'], r['bp'], r['o2'])
        duration = estimate_treatment_time(prio)
        processed.append({
            "id": r['id'], "name": r['name'], "base_priority": prio, "current_priority": prio,
            "total_treatment_time": duration, "remaining_time": duration, "arrival_time": 0, "waiting_in_lobby": 0
        })
    st.session_state.patient_database = processed

# --- STEP 1: CLEAN HAND-CRAFTED REGISTRATION FORM ---
st.subheader("👤 New Patient Admission")
with st.container(border=True):
    form_col1, form_col2 = st.columns(2)
    
    with form_col1:
        new_name = st.text_input("Full Name", placeholder="e.g., Rohan Mehra")
    with form_col2:
        condition = st.selectbox("Chief Medical Complaint", [
            "Normal Routine Checkup / Minor Issue", 
            "Mild Fever & Persistent Cough", 
            "Acute Chest Pain / Respiratory Distress", 
            "Trauma Injury / Severe Hemorrhage"
        ])

    # Dynamic vital preset loader based on human choices
    if "Acute" in condition or "Trauma" in condition:
        o2_val, hr_val, bp_val = 87, 130, 185
        st.error("⚠️ System Note: High-urgency vitals will be mapped automatically.")
    else:
        o2_val, hr_val, bp_val = 98, 75, 120
        st.success("ℹ️ System Note: Standard baseline vitals will be mapped.")

    # Centered Minimal Button
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        submit_btn = st.button("Add to Waiting Room", use_container_width=True)

if submit_btn:
    if new_name.strip() == "":
        st.warning("Please enter a valid patient name.")
    else:
        prio = calculate_triage_score(hr_val, bp_val, o2_val)
        duration = estimate_treatment_time(prio)
        next_id = f"P{len(st.session_state.patient_database) + 1:02d}"
        
        new_p = {
            "id": next_id, "name": new_name, "base_priority": prio, "current_priority": prio,
            "total_treatment_time": duration, "remaining_time": duration, "arrival_time": 0, "waiting_in_lobby": 0
        }
        st.session_state.patient_database.append(new_p)
        st.toast(f"Success: Added {new_name} to queue.", icon="👤")
        time.sleep(0.5)
        st.rerun()

# --- STEP 2: PREMIUM LOBBY CARD LAYOUT ---
st.markdown("---")
st.subheader("⏳ Patients Currently in Queue")

# Render via humanized native block layout
for p in st.session_state.patient_database:
    with st.container(border=True):
        col_left, col_right = st.columns([3, 1])
        
        with col_left:
            st.markdown(f"### {p['name']}")
            st.caption(f"Patient ID: {p['id']} • Expected Duration: {p['total_treatment_time']} mins")
        
        with col_right:
            # Clean context badges instead of ugly tables
            if p['current_priority'] == 1:
                st.error("🚨 Critical")
            elif p['current_priority'] in [2, 3]:
                st.warning("⚠️ Urgent")
            else:
                st.success("🟢 Stable")

# --- STEP 3: WORKSPACE SIMULATION ---
st.markdown("---")
start_sim = st.button("🚀 Execute Doctor Live Scheduling Loop", use_container_width=True)

if start_sim:
    st.subheader("🎬 Active ER Operations Tracker")
    
    ready_queue = copy.deepcopy(st.session_state.patient_database)
    current_patient = None
    current_time = 0
    
    # Modern Native Placeholders
    clock_spot = st.empty()
    active_spot = st.empty()
    waiting_box = st.empty()
    
    while ready_queue or current_patient:
        # Dynamic DAA Sort Integration
        if ready_queue:
            ready_queue = merge_sort(ready_queue)
            
        # Context Switch Logic
        if current_patient is None and ready_queue:
            current_patient = ready_queue.pop(0)
            
        # Top Small Clock
        clock_spot.caption(f"⏱️ HOSPITAL TIMELINE METRIC: {current_time} MINUTES ELAPSED")
        
        # Display Workspace
        if current_patient:
            current_patient['remaining_time'] -= 1
            with active_spot.container(border=True):
                st.markdown(f"## 🩺 Doctor's Unit: Now Treating **{current_patient['name']}**")
                st.progress(max(0, current_patient['remaining_time']) / current_patient['total_treatment_time'])
                st.info(f"Remaining treatment duration needed: **{current_patient['remaining_time']} mins**")
        else:
            active_spot.info("No active patient under care. Doctor Core is currently Idle.")
            
        # Display Next In Line previews smoothly
        if ready_queue:
            with waiting_box.container(border=True):
                st.markdown("#### 📋 Next up in line for treatment:")
                for wp in ready_queue:
                    tag = "🔴 Critical" if wp['current_priority'] == 1 else ("🟡 Urgent" if wp['current_priority'] in [2,3] else "🟢 Stable")
                    st.text(f"→ {wp['id']} : {wp['name']} [{tag}]")
        else:
            waiting_box.empty()
            
        current_time += 1
        time.sleep(1.0)
        
        if current_patient and current_patient['remaining_time'] == 0:
            current_patient = None
            
    st.balloons()
    st.success("🏁 All registered operations handled. ER queue is empty!")