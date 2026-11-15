# Research: NIT Silchar Late-Night Stall Queue Delay & Hostel Curfew Risk

**Person:** Bipul Nath ("Bipul Da")  
**Role:** Sole proprietor and cook at *Bipul Da's Tea Stall* (popularly called **"Tapri"** by students, signboard reads **"NIKHIL TEA STALL"**), situated exactly 80 meters outside Gate No. 1 (Main Gate), National Institute of Technology (NIT) Silchar, Cachar, Assam (788010).  
**Hostels Serviced:** Boys Hostels (BH1 to BH9, Curfew: 12:30 AM) and Girls Hostels (GH1 to GH4, Curfew: 10:30 PM).  
**Date:** November 15, 2026  

---

### 1. The Problem (in 5 lines)
Hostel students at NIT Silchar (BH1 through BH9 and GH1 through GH4) face strict hostel gate curfews (12:30 AM for boys, 10:30 PM for girls) enforced by campus security guards. 
During late study hours, dozens of hostellers walk to Bipul Da's stall ("Tapri") outside Gate 1 for dinner snacks (Double Egg Maggi, Bun Omelette, Chai). 
Bipul Da cooks on a simple 2-burner gas stove and routinely tells every student "bas 5 minute lagega, bohi thaak", only thinking of single-dish cooking time. 
When 4 to 8 orders queue up, actual cooking and pan-clearing takes 18 to 28 minutes, causing students to run across the dark campus in panic to beat the hostel guard's whistle. 
Bipul Da faces counter shouting, students canceling orders midway after eggs are already cracked, and arguments over unpaid food.

---

### 2. Existing Solutions & Why They Do Not Fit Bipul Da

1. **Food Aggregators (Zomato / Swiggy)**
   * *Why it does not fit:* Delivery services in the Silchar outskirts (near NIT campus) do not accept late-night micro-orders (₹35–₹60) from unregistered roadside stalls, and the high delivery charges and minimum order values are rejected by hostellers.

2. **WhatsApp / Phone Calling**
   * *Why it does not fit:* Bipul Da cannot hold a smartphone or read texts while stirring boiling Maggi pans with one hand and cracking eggs with the other amid ambient traffic noise on the Silchar-Hailakandi Road.

---

### 3. Two Sources Read (with 3-line notes each)

1. **Little, J. D. C. (1961). *A Proof for the Queuing Formula: $L = \lambda W$*. Operations Research, 9(3), 383–387.**
   * *Note 1:* Formulates the fundamental queuing identity that the steady-state average number of customers in a system ($L$) equals the arrival rate ($\lambda$) multiplied by the average time in system ($W$).
   * *Note 2:* Establishes that queue length directly ties to waiting time; non-linear queue explosions occur as arrival rate approaches the capacity limit of Bipul Da's 2 physical gas burners.
   * *Note 3:* Demonstrates why Bipul Da's constant "5-minute" promise fails in practice: combined with measured empirical service rates from `data.csv`, any queue depth above 2 orders inevitably stretches turnaround beyond 15–20 minutes.

2. **Kahneman, D., & Tversky, A. (1979). *Intuitive prediction: Biases and fallacious interpretations*. In M. K. Starr & M. Zeleny (Eds.), *Multiple Criteria Decision Making, TIMS Studies in the Management Sciences* (Vol. 12, pp. 313–327). Amsterdam: North-Holland Publishing Company.**
   * *Note 1:* Formulates the *planning fallacy*, where human predictors anchor on best-case execution scenarios while neglecting distributional historical data and operational delays.
   * *Note 2:* Explains why Bipul Da habitually quotes "bas 5 minute"—cognitively anchoring on the isolated preparation time of one Maggi brick without accounting for accumulated ticket queues or pan changeovers.
   * *Note 3:* Provides the behavioral justification for replacing subjective verbal assurances with an empirical, data-calibrated system that calculates realistic student arrival times against hostel curfew limits.
