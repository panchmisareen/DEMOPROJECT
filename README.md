# 🌱 EcoPulse Ultimate Hub
> **Designed and Developed with Pride by Team Invicta Chaos**  
> **Team Members:** Sneha K., Aditi J., Divyanshi D., & Panchmi S.

EcoPulse is a state-of-the-art campus wellness, carbon reduction, creative freedom, and digital detox web platform built specifically for students. It unifies individual cognitive recovery with climate accountability through gamified diagnostics, interactive offline utilities, and a community student exchange.

---

## ✨ Features Overview

### 1. 📊 Dual Diagnostic & AI Recommendations
- **Better Us (Wellness & Burnout Shield)**: Real-time clinical evaluation of sleep duration, screen exposure, self-reported stress (1-10 slider), daily mood, and hydration deficiency to compute a calibrated Burnout Risk Index (0-100).
- **Better Surroundings (Eco Footprint Engine)**: Tracks campus travel modes (Walking, Cycling, Shuttle, EV, Carpool, Cab) and daily diet choices to calculate precise kilograms of CO₂ emitted, laptop charge equivalents, and total carbon prevented vs an inefficient baseline.
- **Dynamic Interventions**: Auto-pairs your fatigue state with tailored zero-equipment dorm workouts, plant-based power recipes, and habit interventions.

### 2. 🌿 Virtual Eco Companion & Gamification
- Dynamic Tamagotchi-style evolving companion (Seedling ➔ Young Sprout ➔ Flowering Pot ➔ Blooming Tree ➔ Planet Guardian Tree).
- Real-time XP gain system, level progression, dual streaks (Wellness + Climate), single-use plastics counter, and downloadable CSV activity history.

### 3. 🧘 Zen & Ambient Lounge
- **100% Offline Synthesizer** using the Web Audio API: Rain Shower, Ocean Waves, Forest Canopy Wind, Brown Noise (deep study frequency), and Tibetan Singing Bowls (432Hz harmonic chime).
- **4-7-8 Guided Breathing Circle**: Parasympathetic vagus nerve reset with animated visual pulsing.
- **Daily Inspiration & Affirmations**: Curated quotes for student mental resilience.

### 4. 🎨 Creative Doodle Studio & Literary Corner
- **HTML5 Freehand Canvas**: Smooth brush strokes, custom palette presets, eraser, undo stack, PNG export, and **Publish to Community Gallery** (+25 XP).
- **Student Literary Corner**: Submit and share original verses, poems, and reflections. Interactive peer like system (+5 XP).

### 5. 📚 Book Lovers Haven
- Distraction-free reader preloaded with timeless public domain classics (*Alice in Wonderland*, *Walden by Thoreau*, *Meditations by Marcus Aurelius*, *The Art of War*, and *Sherlock Holmes*).
- Typography scaling (A- / A+) and Paper/Night reading modes.

### 6. 🎮 Brain Arcade & Puzzles
- **Endless Speed Math Engine**: Rapid mental arithmetic to cure afternoon study fatigue with instant audio feedback.
- **Climate & Logic Riddles**: Thought-provoking riddles with interactive hints and fuzzy verification.
- **Eco Memory Match Card Game**: 12-card flipping game with cheerful feedback and completion rewards.

### 7. ⏱️ Digital Detox & Deep Focus Lock
- Unmindful doomscrolling assessment and attention span penalty dial.
- Fullscreen immersive lock screen overlay with countdown timers (15m, 25m Pomodoro, 45m deep study) and emergency exit protections.

### 8. 🥗 Gourmet Eco-Kitchen & 🏋️ Dorm Workout Arena
- Filterable student dorm recipes with time, macro split (calories/protein), and step-by-step cooking steps.
- Fatigue-adaptive workouts (Restorative for high fatigue, Core & Strength for moderate, HIIT for low fatigue).

### 9. 🎯 Daily Mindful Missions & Campus Badges
- Daily quests (e.g. hydration targets, active transit, plant-based lunch) with instant XP claims.
- Achievement badges system honoring your campus eco milestones.

---

## 🚀 How to Run the App

### Requirements
- Python 3.10+
- Flask (`pip install -r requirements.txt`)

### Startup
Open your terminal and navigate to the project directory:

```bash
cd /Users/panchmisareen/Desktop/ecopulse
python3 app.py
```

Then visit in your web browser:
```
http://localhost:5050
```

---

## 🛠️ Technology Stack
- **Backend**: Python 3, Flask, SQLite3 (persistent in `data/ecopulse.db`), CSV reporting.
- **Frontend**: Semantic HTML5, CSS3 Variables & Glassmorphism design system (Dark & Light theme support).
- **Client Logic**: Vanilla JavaScript ES6+, Web Audio API (real-time sound synthesis), HTML5 Canvas API (interactive doodle pad).
- **Privacy**: 100% local, offline-ready, zero tracking or external CDN dependencies.
