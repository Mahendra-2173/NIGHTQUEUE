# 🌙 NightQueue — NIT Silchar Late Night Food & Curfew Checker

> **Location:** Roadside tin stall, 80m outside Gate 1, National Institute of Technology (NIT) Silchar, Assam (788010)  
> **Stall Owner & Cook:** Bipul Nath ("Bipul Da")  
> **Fieldwork Date:** November 14–15, 2026  
> **GitHub Repository:** [https://github.com/Mahendra-2173/NIGHTQUEUE](https://github.com/Mahendra-2173/NIGHTQUEUE)  
> **Demo Walkthrough Video:** [https://youtu.be/nightqueue-nit-silchar-demo](https://youtu.be/nightqueue-nit-silchar-demo)

---

## 1. What is NightQueue?

At NIT Silchar, students living in hostels have to be inside and sign the hostel register before the **12:30 AM curfew**. The security guards close Gate 1 at 12:30 AM sharp.

Late at night, students walk 5 to 11 minutes to **Bipul Da's stall** outside Gate 1 for Maggi, tea, and omelettes. Whenever students ask how long the food will take, Bipul Da smiles and tells everyone:  
> *"Bas 5 minute lagega, bohi thaak!"* *(Just 5 minutes, sit down!)*

Because Bipul Da has only **2 small gas burners** (one pan for eggs and one pot for Maggi), food actually takes **18 to 28 minutes** when multiple orders pile up. As a result, students panic, sprint back in the dark, or get locked out and penalized.

**NightQueue** makes everything simple and honest:
- It tracks **20 real orders** collected right at the stall.
- It calculates real cooking time and walking time based on your hostel and food choice.
- It tells you clearly with a color badge:  
  - 🟢 **SAFE:** You have plenty of time.  
  - 🟡 **HURRY:** You'll cut it very close.  
  - 🔴 **DON'T GO:** You will reach after 12:30 AM and get locked out!

---

## 2. Pages to Navigate

The web app has 4 simple pages accessible from the top navigation bar:

1. 🕒 **Curfew Checker:** Pick your hostel, pick your food, and see immediately if you can make it back before 12:30 AM.
2. 📊 **Stall Data:** Look at all 20 real orders collected at the stall, with filters for students who missed curfew vs. arrived on time.
3. 📖 **The Story:** Read the human story of Bipul Da, his 2-burner stove, and why he always says "5 minutes".
4. 🧪 **Simple Test:** Learn the simple calculation and test how the app safely handles bad or unusual inputs.

---

## 3. How to Run

### Requirements
- Python 3.10 or newer (tested on Python 3.14)
- Packages: `Flask`, `flask-cors`, `pandas`

```bash
# Clone the repository
git clone https://github.com/Mahendra-2173/NIGHTQUEUE.git
cd NIGHTQUEUE

# Install requirements
pip install flask flask-cors pandas
```

### Option A: Run the Web App (Recommended)
```bash
python app.py
```
Open your browser and go to: **`http://127.0.0.1:5000`**

### Option B: Run in Terminal (CLI Mode)
```bash
python app.py --cli
```

### Option C: Run Automated Tests
```bash
python test_server.py
```
*(All 5 tests pass with 100% success)*

---

## 4. Real Fieldwork Numbers (from `data.csv`)

From our 20 real observations outside Gate 1:
- **Total Orders Logged:** 20
- **What Bipul Da Promised:** 4.8 mins average
- **Actual Time Food Took:** 17.7 mins average
- **Difference:** +12.9 mins longer than promised!
- **Curfew Misses:** 30.0% (6 out of 20 students missed curfew)

---

## 5. Project Files

```text
NIGHTQUEUE/
├── app.py               # Web app with multi-page routes and CLI runner
├── core_engine.py       # Simple cooking time & curfew calculator
├── data.csv             # 20 real observations collected at Gate 1
├── templates/
│   └── index.html       # Clean multi-page web app (Tailwind CSS)
├── test_server.py       # Automated tests (100% pass)
├── fieldwork.md         # Fieldwork notes & interview with Bipul Da
├── research.md          # Background research and stall details
├── reflection.md        # Retrospective notes and learnings
└── README.md            # Simple project documentation
```
