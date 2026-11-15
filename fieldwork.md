# Fieldwork: Bipul Da's Night Stall outside Gate 1, NIT Silchar

**Location:** Roadside tin-shed stall, 80 meters outside Gate 1 (Main Gate), National Institute of Technology (NIT) Silchar, Cachar, Assam (788010).  
**Date & Time:** November 14–15, 2026, 23:20 to 00:15 IST (Late-Night Rush Window).  
**Person Interviewed:** Bipul Nath ("Bipul Da"), age 44, owner & sole cook.  

---

### 1. On-Site Observation Context
* Stood directly beside the stall counter next to the wooden water barrel from 23:20 to 00:15 IST during the peak pre-curfew rush.
* Bipul Da operates a two-burner commercial LPG stove under a low tin shed.
* Burner 1 holds an iron tawa dedicated to frying eggs, toasting bread, and buttering local pao buns.
* Burner 2 holds a cylindrical aluminium saucepan for boiling water and preparing Maggi noodles.
* Between 23:30 and 00:10, a dense cluster of 6 to 10 hostellers continuously crowded the narrow roadside counter, discussing impending semester exams while watching the stove flame.

---

### 2. The Conversation with Bipul Da

* **3 Things He Said:**
  1. *"Sobai ke jodi boli 20 minute lagbo, student shob choliya jabo ba canteen bondho bhabi loibo. Tai boli 5 minute, bohi thaako."*  
     *(“If I tell everyone it will take 20 minutes, all students will leave or think the canteen is closed. So I tell them just 5 minutes, sit down and wait.”)*
  2. *"Duta pan ase. Ekta te omlet banale ar Maggi banano jaay na. Tel aar paani eksaathe meshano jaay na re bhai."*  
     *(“I have two pans. If I fry an omelette on one, I cannot make Maggi in it immediately. You cannot mix oil and boiling water together, brother.”)*
  3. *"12:20 AM er por hostel guard whistle bajay Gate 1 e. Okhon shob lora ghabraye jaay aar amake ghaare daari thakiya taagaada deye."*  
     *(“After 12:20 AM, the hostel security guard starts blowing the whistle at Gate 1. That’s when the boys panic and literally breathe down my neck at the stove.”)*

* **1 Thing That Surprised Me:**
  * I initially assumed the delay was purely cooking time (the 2-minute Maggi taking 4 minutes). What actually killed his turnaround time was **pan transition latency**. Whenever someone ordered an Egg Toast after a Maggi, Bipul Da had to wipe down the tawa with a coarse jute rag, apply oil, let the surface smoke, and whisk eggs in a steel mug. This sanitation and changeover took **60 to 90 seconds of zero-cooking dead time** between discordant food categories, an overhead invisible to the waiting students.

---

### 3. Data Collection Methodology
* **How Collected:** Stood with a phone notepad on the side wooden bench next to Bipul Da's water jar between 23:25 and 00:10 IST.
* For each customer arrival:
  1. Recorded exact timestamp when the order was voiced.
  2. Recorded Bipul Da's verbal commitment (`claimed_wait_mins`).
  3. Counted the physical queue of pending tickets ahead at that second (`queue_ahead`).
  4. Tracked the exact moment the hot paper plate was handed over (`actual_wait_mins`).
  5. Logged whether the student experienced curfew-related friction, sprinted towards Gate 1, or was logged into the late register (`curfew_breach`).
* Raw entries are stored in [`data.csv`](data.csv).
