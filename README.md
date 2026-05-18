# 🩺 LifeLine: Hospital Emergency Triage Engine

An interactive, dual-interface software ecosystem mapping clinical data parameters into Data Structures & Algorithms (DAA) and Operating Systems (OS) Process Management abstractions.

---

## 🛠️ Main Features Implemented

1. **Clinical Triage Scoring Engine:** Normalizes physiological vitals (Oxygen, Heart Rate, BP) directly into ESI priority scales.
2. **DAA Batch Comparisons:** Implements both `Selection Sort` ($O(n^2)$) and `Merge Sort` ($O(n \log n)$) to display performance execution metrics.
3. **OS CPU Scheduling Abstraction:** Models patients as active processes, running a non-preemptive Priority Scheduling Engine with a single doctor acting as the CPU core.
4. **Starvation Prevention (Aging):** Increases patient priority dynamically if they sit inside the ready queue lobby past designated thresholds.
5. **Dynamic Door Arrivals:** Injects new patient processes mid-simulation loop to verify live re-sorting metrics.

---

## 🚀 Execution Instructions

### Prerequisites
Ensure Python 3.8+ is installed on your local computer, then run the terminal command below to download the pandas and streamlit dashboard rendering packages:
```bash
pip install streamlit pandas