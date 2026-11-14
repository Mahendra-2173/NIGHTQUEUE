# Reflection (Step 4)

### What I Got Wrong at the Start
When I first picked this problem, I assumed Bipul Da’s delay was a straightforward food-delivery scheduling problem. I thought about building a pre-order token system where students would book a slot from their hostel room and he would cook it in order. 

Sitting outside Gate 1 in the cold for 20 minutes completely dismantled that idea. Bipul Da doesn't have time to look at a screen, let alone manage time slots. If someone orders online and doesn't show up, he loses ₹50. More importantly, I thought cooking speed was the sole bottleneck. Watching him cook revealed the real bottleneck was *sanitation between dish types*: cleaning egg grease off the tawa before toasting butter buns or boiling Maggi took 60 to 90 seconds of zero-cooking dead time. My initial mathematical model didn't even have a term for pan transition latency.

### What I Would Cut
If I had to redo this under tighter time constraints, I would cut out the multi-category dish breakdown in the UI. 90% of late-night panic orders at NIT Silchar are either Double Egg Maggi or Bun Omelette. Collapsing the menu to just "Maggi vs. Egg Tawa" would simplify the input to a single binary toggle and make the model faster to tune without losing much predictive accuracy. I would also remove the custom hostel walking map selector and just default to an 8-minute average radius, since students rarely check their exact walking pace.

### Where AI Helped
AI was genuinely useful in two places:
1. Translating Little’s Law and multi-server queue formulas into concise Python dataclasses within 15 minutes.
2. Generating the responsive Tailwind CSS layout and styling for `templates/index.html`, which would have taken me 2 hours of tedious manual CSS flexbox alignment.

### Where AI Wasted Time
AI tried to over-engineer the core problem from the very beginning. When I first asked it for advice, it kept proposing XGBoost regression models, LSTM time-series forecasting, and an end-to-end React native app with Twilio SMS integration. All of that was completely useless for a 20-row real dataset and a vendor who doesn't even have a smartphone mount on his cart. 

It also generated an unquoted comma inside my CSV notes on row 9 (`'Bipul Da, hoise?'`), which broke the Pandas C-parser with an extra column error that cost me 15 minutes of manual debugging. I had to rein the AI back and force it to stick to clean, deterministic operational physics rather than bloated buzzword architecture.
