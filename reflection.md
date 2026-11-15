# Reflection (Step 4)

> **Live Deployment:** [https://nightqueue.onrender.com](https://nightqueue.onrender.com)  
> **GitHub Repository:** [https://github.com/Mahendra-2173/NIGHTQUEUE](https://github.com/Mahendra-2173/NIGHTQUEUE)  
> **3-Minute Screen Recording Video:** [Watch on Google Drive](https://drive.google.com/drive/folders/1zBrTpkhPoQvqBuyldZZNyvc1oD0mFReR?usp=drive_link) *(Companion mirror: [`demo.mp4`](demo.mp4))*  

---

### What I got wrong at the start
When I first started thinking about this project, I thought I would build a simple pre-ordering token app where students could book a slot from their hostel room and pick up their food when ready. 

Once I actually walked out to Gate 1 at 11:30 PM in the cold and sat on the wooden bench, I realized how bad that idea was. Bipul Da’s hands are covered in cooking oil and egg batter—he doesn't have time to look at a phone screen. If someone books an order from their room and falls asleep, Bipul Da loses ₹50 of his own money on wasted eggs and Maggi. 

Also, I assumed cooking time was the only delay. But watching him cook, I saw that every time someone ordered an egg toast after Maggi, he had to stop, take a rough cloth, and wipe down the hot tawa to clean off the grease before toasting the buns. That cleaning step took almost a minute and a half of dead time where nothing was cooking. I had completely missed that when planning in my room.

### What I would cut
If I had to do this again with less time, I would cut down the menu items. Honestly, 90% of students at that hour just order Double Egg Maggi or Bun Omelette. Having tea and multiple variations just made my code and dropdown bigger without changing much. I would also remove the custom hostel walking selector and just default to an average 8-minute walk, because nobody at midnight is checking their exact walking pace.

### Where AI helped
AI was helpful for writing the messy frontend code. Generating the Tailwind CSS for the dark mode cards and layout saved me at least two hours of painful CSS alignment. It was also useful for fixing a tricky Python datetime bug: when an order was placed at 23:55 and the curfew was 00:30, my code kept subtracting them and giving -1405 minutes because Python thought 00:30 belonged to yesterday morning. AI helped me structure the date anchor to handle the midnight rollover cleanly.

### Where AI wasted time
AI kept trying to overcomplicate everything. When I first asked for ideas, it kept suggesting that I build an XGBoost machine learning model, an LSTM neural network, or a React Native mobile app with Twilio SMS alerts. That made zero sense for a roadside tapri and a 20-row real dataset. 

It also messed up row 9 in my CSV by putting an unquoted comma inside the note (`Bipul Da, hoise?`), which caused Pandas to throw a column mismatch error that took me 15 minutes of manual line-by-line checking to fix. I had to stop asking it for high-level advice and just use it to write specific small helper functions.
