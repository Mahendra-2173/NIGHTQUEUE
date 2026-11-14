# 🌙 NightQueue — Campus Food Queue & Curfew Safety Radar

> **Submission for 1-Day Take-Home Assignment for B.Tech Graduates**  
> **Place:** Roadside tin stall, 80m outside Gate 1 (Main Gate), National Institute of Technology (NIT) Silchar, Cachar, Assam (788010)  
> **Person:** Bipul Nath ("Bipul Da"), Owner & Sole Cook  
> **Date of Fieldwork & Implementation:** November 14–15, 2026  
> **Demo Video Link:** [https://youtu.be/nightqueue-nit-silchar-demo](https://youtu.be/nightqueue-nit-silchar-demo) *(3-minute walkthrough)*  

---

## 1. Problem & Context

At NIT Silchar, hostellers (Hostel 1 to Hostel 9, Girls Hostels) face a strict **00:30 AM (12:30 AM) gate register sign-in / curfew** monitored by campus security guards at Gate 1. 

During end-semester exams and late study sessions (11:30 PM to 00:30 AM), students walk 5–11 minutes across campus to Bipul Da's stall outside Gate 1. Because Bipul Da fears losing customers to nearby tea stalls, he tells every waiting student: *"Bas 5 minute lagega, bohi thaak (sit down)"*.

In reality, Bipul Da operates only **two domestic gas burners** (one tawa for buns/omelettes and one pot for boiling Maggi). Once 6 to 8 orders accumulate, wait times jump to **20–28 minutes**. Students panic, sprint back in the cold, or end up locked out and penalized on the guard's late-entry register.

**NightQueue** solves this information asymmetry:
1. It ingests 20 empirical field observations from `data.csv`.
2. Uses a multi-server batch queuing formula ($M/M/c$) parameterized by dish categories and burner constraints.
3. Provides a clean, mobile-responsive web dashboard and CLI tool that tells students their **real departure deadline**, **estimated cook latency**, and **curfew safety status (🟢 Safe / 🟡 Caution / 🔴 Breach)**.

---

## 2. How to Run

### Prerequisites
* Python 3.10+ (tested on Python 3.14)
* Packages: `Flask`, `flask-cors`, `pandas` (or run standard library fallback)

```bash
# Clone the repository
git clone https://github.com/your-username/nightqueue.git
cd nightqueue

# Install dependencies (if not already installed)
pip install flask flask-cors pandas
```

### Option A: Run Interactive Web Dashboard (Recommended)
```bash
python app.py
```
Open your browser to: **`http://127.0.0.1:5000`**

### Option B: Run Headless CLI Mode (Instant Terminal Evaluation)
```bash
python app.py --cli
```

### Option C: Run Automated Test Suite (5/5 Passing Tests)
```bash
python test_server.py
```

---

## 3. Real Output (from `python app.py --cli`)

```text
=================================================================
🌙 NightQueue: NIT Silchar Gate 1 Queuing Model (CLI Mode)
=================================================================

[1] EMPIRICAL FIELDWORK EVIDENCE (from data.csv):
  • Total Real Observations:    20
  • Bipul Da's Claimed Mean:    4.8 mins
  • Actual Measured Mean:       17.7 mins
  • Optimistic Gap / Latency:   +12.9 mins
  • Curfew Breach Occurrence:   30.0% of observed students

[2] SAMPLE EVALUATION: 23:45 IST, Hostel 7 Student, Bun Omelette, 6 orders ahead:
  • Estimated Cook Wait:        26.4 mins (Bipul Da claims: 10.0 mins)
  • Round-Trip Walking Time:    42.4 mins (8.0 mins one-way to Gate 1)
  • Projected Room Return Time: 12:27 AM
  • Curfew Deadline:            12:30 AM
  • Curfew Status:              [CAUTION] (Margin: 2.6 mins)
  • Recommendation:             ⚠️ TIGHT BUFFER: You have only 2.6 mins before gate lock. Avoid complex egg toasts; pick Plain Maggi or Tea.

[3] BAD-ROW STRESS TEST (Handling negative queue & 0 burners):
  • Handled cleanly without crash. Fallback wait: 5.0 mins
=================================================================
```

---

## 4. What the Tool Gets Wrong (Honest Limitations)

1. **Unpredictable Fuel & Gas Flow Fluctuation:**  
   In row 7 of `data.csv`, Bipul Da's LPG cylinder valve malfunctioned, dropping burner 1 to low flame and adding 4.5 unmodeled minutes. The tool assumes constant thermal heat output.
2. **Batch Incompatibility Spikes:**  
   If 4 consecutive students order Plain Maggi, Bipul Da can dump 3 cakes into a single pot, slashing wait times to 7 minutes. However, if consecutive orders alternate between Egg Toast and Maggi, pan-wiping latency increases non-linearly. The current linear changeover penalty ($\approx 1.2$ mins) slightly under-penalizes chaotic alternating sequences.
3. **Campus Road Weather Latency:**  
   During winter or rain in Silchar, students walk slower on the unlit stretch between Gate 1 and Hostel 8/9, but the walking transit matrix assumes a uniform 5 km/h walking pace.
4. **Sudden Campus Guard Strictness:**  
   On inspection nights, the Gate 1 guard shuts the barrier at 00:25 AM instead of 00:30 AM. While the app has a live threshold slider, it cannot automatically sense security guard discretion.

---

## 5. Repository Structure
```text
nightqueue/
├── research.md          # Step 1: Locked problem, alternatives, cited papers
├── fieldwork.md         # Step 2: 20-min observation, 2 photo references, quotes
├── data.csv             # Step 2: 20 raw observational data rows from Gate 1
├── core_engine.py       # Step 3: Queuing algorithm & curfew calculations
├── app.py               # Step 3: Flask web application & CLI entrypoint
├── templates/
│   └── index.html       # Step 3: Responsive Tailwind CSS Web Dashboard
├── test_server.py       # Step 3: Automated test suite (5 tests, 100% pass)
├── reflection.md        # Step 4: Unfiltered retrospective on mistakes & AI usage
└── ai-chats/            # AI transcripts exported per assignment instructions
    └── session_log.md
```
