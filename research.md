# Research: NIT Silchar Late-Night Stall Wait-Time & Hostel Curfew Breach

**Person:** Bipul Nath ("Bipul Da")  
**Role:** Sole proprietor and cook at *Bipul Da's Night Canteen & Tea Stall*, situated just outside Gate No. 1 (Main Gate), NIT Silchar, Cachar, Assam (788010).  
**Date:** November 15, 2026  

---

### 1. The Problem (in 5 lines)
Hostel students at NIT Silchar (Hostel 6, Hostel 7, and Hostel 8) face a strict late-night hostel register sign-in and gate curfew at 00:30 AM (12:30 AM) monitored by campus security guards. 
During late study hours, dozens of hostellers walk 400–600 meters to Bipul Da's stall outside Gate 1 for dinner snacks (Egg Maggi, Bun Omelette, Lal Saah/Chai). 
Bipul Da cooks on a simple 2-burner commercial gas stove and systematically underestimates preparation delays, telling every anxious student "bas 5 minute lagega, bohi thaak (sit down)". 
When 6 to 8 orders queue up, actual cooking and pan-clearing takes 20 to 28 minutes, causing students to run across the dark campus road in panic to beat the hostel guard's whistle. 
Bipul Da faces constant counter shouting, students canceling orders midway when the 00:15 AM warning bell strikes, and chaotic disputes over UPI payments.

---

### 2. Existing Solutions & Why They Do Not Fit Bipul Da

1. **Food Aggregators (Zomato / Swiggy)**
   * *Why it does not fit:* Delivery services in the Silchar outskirts (near NIT campus) do not accept late-night micro-orders (₹35–₹60) from unregistered roadside stalls, and the high delivery charges and minimum order values are rejected by hostellers.

2. **WhatsApp / Phone Calling**
   * *Why it does not fit:* Bipul Da cannot hold a smartphone or read texts while stirring boiling Maggi pans with one hand and cracking eggs with the other amid ambient traffic noise on the Silchar-Hailakandi Road.

---

### 3. Two Sources Read (with 3-line notes each)

1. **Little, J. D. (1961). *A Proof for the Queuing Formula: $L = \lambda W$*. Operations Research, 9(3), 383–387.**
   * *Note 1:* Formulates that average waiting queue ($L$) equals arrival rate ($\lambda$) multiplied by average service wait time ($W$).
   * *Note 2:* Confirms that queue length blows up non-linearly as arrival rate approaches the combined cooking service rate of Bipul Da's 2 burners.
   * *Note 3:* Proves that Bipul Da's universal "5 minute" claim is mathematically impossible once the pending queue exceeds 2 orders.

2. **Kahneman, D., & Tversky, A. (1979). *Intuitive prediction: Biases and fallacious interpretations*. Studies in Management Science, 12, 313–327.**
   * *Note 1:* Formalizes the planning fallacy and cognitive estimation bias where individuals project best-case scenarios while systematically ignoring past operational friction.
   * *Note 2:* Explains why roadside stall operators in campus environments instinctively quote "5 minutes" to avoid losing impatient students to rival stalls.
   * *Note 3:* Provides the operational foundation for an objective, algorithm-driven wait calculator that removes human optimism bias.
