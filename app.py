from flask import Flask, request, render_template, jsonify, make_response
import random
import datetime
import io
import csv
import data_manager

app = Flask(__name__)

# =========================================================
# EMISSION FACTORS & METRICS
# =========================================================
EMISSION_FACTORS = {
    'transport': {
        'bike_walk': 0.0,
        'bus': 0.075,
        'ev': 0.045,
        'carpool': 0.095,
        'car': 0.21
    },
    'diet': {
        'vegan': 0.6,
        'vegetarian': 0.85,
        'pescatarian': 1.45,
        'balanced': 1.85,
        'meat': 3.55
    }
}

TRANSPORT_NAMES = {
    'bike_walk': 'Bicycle / Walking (Zero CO₂)',
    'bus': 'Public Bus / Campus Shuttle',
    'ev': 'Electric Vehicle / Campus Cart',
    'carpool': 'Shared Carpool / Transit Van',
    'car': 'Cab / Solo Motor Car'
}

DIET_NAMES = {
    'vegan': 'Plant-Based / Vegan',
    'vegetarian': 'Vegetarian Dish',
    'pescatarian': 'Pescatarian (Fish & Greens)',
    'balanced': 'Balanced Dish (Poultry / Dairy)',
    'meat': 'Red Meat Heavy Dish'
}

def evaluate_burnout(sleep, screen, stress, mood="focused", water=7):
    """Computes a nuanced Burnout Risk Index (0-100) and provides clinical wellness guidance."""
    score = 0

    # Sleep impact
    if sleep < 5.0: score += 32
    elif sleep < 6.5: score += 20
    elif sleep < 7.5: score += 6
    elif sleep > 10.0: score += 10 # Hypersomnia exhaustion

    # Screen impact
    if screen > 10.0: score += 30
    elif screen > 8.0: score += 18
    elif screen > 6.0: score += 8

    # Stress impact (1-10)
    score += int(stress * 3.8)

    # Mood adjustment
    mood_adjustments = {
        'exhausted': 18,
        'anxious': 12,
        'neutral': 4,
        'focused': -6,
        'energetic': -12
    }
    score += mood_adjustments.get(mood.lower(), 0)

    # Hydration deficiency
    if water < 4: score += 10
    elif water >= 8: score -= 5

    # Clamp score
    score = max(5, min(98, score))

    if score >= 65:
        risk = "High"
        risk_class = "high"
        msg = "High cognitive fatigue & stress load detected! Your nervous system needs immediate restoration, hydration, and an offline screen sunset."
    elif score >= 35:
        risk = "Moderate"
        risk_class = "moderate"
        msg = "Moderate fatigue detected. Break up prolonged study stretches with quiet mobility movements and natural hydration."
    else:
        risk = "Low"
        risk_class = "low"
        msg = "Optimal energy and balanced focus! You have excellent stamina today for both deep academic work and active physical fitness."

    return risk, risk_class, msg, score

def calculate_carbon(distance, mode, diet):
    """Computes exact carbon footprint and intuitive student lifestyle equivalents."""
    factor_trans = EMISSION_FACTORS['transport'].get(mode, 0.1)
    factor_diet = EMISSION_FACTORS['diet'].get(diet, 1.85)

    transport_co2 = round(distance * factor_trans, 2)
    diet_co2 = round(factor_diet, 2)
    total_co2 = round(transport_co2 + diet_co2, 2)

    # Student equivalents:
    # 1 full smartphone charge ~ 0.008 kg CO2
    # 1 full laptop charge ~ 0.015 kg CO2
    # 1 km driven in standard petrol car ~ 0.21 kg CO2
    laptop_charges = int(total_co2 / 0.015)
    phone_charges = int(total_co2 / 0.008)

    # Savings compared to typical inefficient baseline (10km solo car + red meat meal = 2.1 + 3.55 = 5.65 kg)
    baseline_co2 = round(distance * 0.21 + 3.55, 2)
    co2_saved = round(max(0.0, baseline_co2 - total_co2), 2)

    return {
        'total_co2': total_co2,
        'transport_co2': transport_co2,
        'diet_co2': diet_co2,
        'laptop_charges': laptop_charges,
        'phone_charges': phone_charges,
        'co2_saved': co2_saved
    }

# =========================================================
# MAIN APP WEB ROUTES
# =========================================================

@app.route('/', methods=['GET'])
def index():
    profile = data_manager.get_user_profile()
    history = data_manager.get_history_logs(limit=15)
    recipes = data_manager.DEFAULT_RECIPES
    workouts = data_manager.DEFAULT_WORKOUTS
    quotes = data_manager.DEFAULT_QUOTES
    books = data_manager.DEFAULT_BOOKS
    quests = data_manager.get_daily_quests()
    badges = data_manager.get_badges()
    posts = data_manager.get_literary_posts()
    doodles = data_manager.get_doodles(limit=30)
    workout_logs = data_manager.get_workout_logs(limit=15)
    workout_stats = data_manager.get_workout_stats()
    reading_progress = data_manager.get_reading_progress()

    return render_template(
        'index.html',
        profile=profile,
        history=history,
        recipes=recipes,
        workouts=workouts,
        quotes=quotes,
        books=books,
        quests=quests,
        badges=badges,
        posts=posts,
        doodles=doodles,
        workout_logs=workout_logs,
        workout_stats=workout_stats,
        reading_progress=reading_progress,
        initial_results=None,
        inputs=None
    )

@app.route('/analyze', methods=['POST'])
def analyze():
    """Form submit endpoint that supports standard POST request or AJAX."""
    try:
        sleep = float(request.form.get('sleep', 7.5))
        screen = float(request.form.get('screen', 7.0))
        stress = int(request.form.get('stress', 4))
        water = int(request.form.get('water', 7))
        mood = request.form.get('mood', 'focused')

        commute_distance = float(request.form.get('commute_distance', 4.0))
        transport_mode = request.form.get('transport_mode', 'bike_walk')
        diet_choice = request.form.get('diet_choice', 'vegetarian')
        refills = int(request.form.get('refills', 4))
    except (ValueError, TypeError):
        sleep, screen, stress, water, mood = 7.5, 7.0, 4, 7, 'focused'
        commute_distance, transport_mode, diet_choice, refills = 4.0, 'bike_walk', 'vegetarian', 4

    burnout_risk, burnout_class, burnout_msg, burnout_score = evaluate_burnout(sleep, screen, stress, mood, water)
    carbon_data = calculate_carbon(commute_distance, transport_mode, diet_choice)

    # Tailored recommendations
    workout_candidates = data_manager.DEFAULT_WORKOUTS.get(burnout_risk, data_manager.DEFAULT_WORKOUTS['Moderate'])
    workout = random.choice(workout_candidates)
    recipe = random.choice(data_manager.DEFAULT_RECIPES)

    interventions = []
    earned_xp = 45

    if transport_mode == 'car':
        saved_kg = round(commute_distance * 0.21, 2)
        interventions.append({
            'title': '🚲 Active Green Campus Commute Swap',
            'desc': f'Your {commute_distance} km car trip emitted ~{saved_kg} kg CO₂. Swapping to walking or campus bike saves emissions and provides 30 mins of cardiovascular rejuvenation!',
            'type': 'Eco Action',
            'badge': '+40 XP'
        })
    elif transport_mode in ['bike_walk', 'ev']:
        earned_xp += 30
        interventions.append({
            'title': '🌟 Zero-Emission Commute Champion',
            'desc': f'Awesome job choosing {TRANSPORT_NAMES.get(transport_mode, transport_mode)}! You prevented tailpipe emissions across your {commute_distance} km trip.',
            'type': 'Affirmation',
            'badge': 'Active'
        })

    if diet_choice in ['vegan', 'vegetarian']:
        earned_xp += 30
    elif diet_choice == 'meat':
        interventions.append({
            'title': '🌱 Plant-Forward Meatless Transition',
            'desc': 'Switching just one red meat meal a day to a legume or tofu bowl reduces your food carbon footprint by over 65% and aids digestion.',
            'type': 'Nutrition',
            'badge': '+35 XP'
        })

    if screen > 8.0:
        interventions.append({
            'title': '🌙 Digital Sunset & Blue Light Filter',
            'desc': f'You logged {screen} hours of screen time today. Set a 15-minute Deep Focus Lock before bed to lower evening cortisol and restore deep sleep cycles.',
            'type': 'Detox Habit',
            'badge': '+25 XP'
        })

    if water < 6:
        interventions.append({
            'title': '💧 Cellular Hydration Target',
            'desc': f'Only {water} glasses logged today. Dehydration reduces cognitive alertness by 12%. Keep your reusable flask at your study desk!',
            'type': 'Hydration',
            'badge': '+20 XP'
        })

    # Update profile in database
    data_manager.update_user_profile(
        xp_add=earned_xp,
        bottles_add=refills,
        co2_saved_add=carbon_data['co2_saved'],
        water_add=max(0, water - 5)
    )

    # Save to history log
    data_manager.add_history_log(
        sleep=sleep,
        screen=screen,
        stress=stress,
        mood=mood.title(),
        transport=TRANSPORT_NAMES.get(transport_mode, transport_mode),
        distance=commute_distance,
        diet=DIET_NAMES.get(diet_choice, diet_choice),
        co2=carbon_data['total_co2'],
        burnout=burnout_risk,
        burnout_class=burnout_class,
        xp_earned=earned_xp
    )

    results = {
        'burnout_risk': burnout_risk,
        'burnout_class': burnout_class,
        'burnout_msg': burnout_msg,
        'burnout_score': burnout_score,
        'co2_total': carbon_data['total_co2'],
        'transport_co2': carbon_data['transport_co2'],
        'diet_co2': carbon_data['diet_co2'],
        'laptop_charges': carbon_data['laptop_charges'],
        'phone_charges': carbon_data['phone_charges'],
        'co2_saved': carbon_data['co2_saved'],
        'earned_xp': earned_xp,
        'workout': workout,
        'recipe': recipe,
        'interventions': interventions
    }

    # If client requested JSON via AJAX:
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        profile = data_manager.get_user_profile()
        return jsonify({
            'success': True,
            'results': results,
            'profile': profile
        })

    # Normal form fallback
    profile = data_manager.get_user_profile()
    history = data_manager.get_history_logs(limit=15)
    quests = data_manager.get_daily_quests()
    badges = data_manager.get_badges()
    posts = data_manager.get_literary_posts()
    doodles = data_manager.get_doodles(limit=30)
    workout_logs = data_manager.get_workout_logs(limit=15)
    workout_stats = data_manager.get_workout_stats()
    reading_progress = data_manager.get_reading_progress()

    inputs = {
        'sleep': sleep, 'screen': screen, 'stress': stress, 'water': water, 'mood': mood,
        'commute_distance': commute_distance, 'transport_mode': transport_mode,
        'diet_choice': diet_choice, 'refills': refills
    }

    return render_template(
        'index.html',
        profile=profile,
        history=history,
        recipes=data_manager.DEFAULT_RECIPES,
        workouts=data_manager.DEFAULT_WORKOUTS,
        quotes=data_manager.DEFAULT_QUOTES,
        books=data_manager.DEFAULT_BOOKS,
        quests=quests,
        badges=badges,
        posts=posts,
        doodles=doodles,
        workout_logs=workout_logs,
        workout_stats=workout_stats,
        reading_progress=reading_progress,
        initial_results=results,
        inputs=inputs
    )

# =========================================================
# JSON REST APIS FOR RICH REAL-TIME CLIENT INTERACTIONS
# =========================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    profile = data_manager.get_user_profile()
    badges = data_manager.get_badges()
    quests = data_manager.get_daily_quests()
    return jsonify({
        'profile': profile,
        'badges': badges,
        'quests': quests
    })

@app.route('/api/water/drink', methods=['POST'])
def drink_water():
    profile = data_manager.update_user_profile(xp_add=15, water_add=1)
    return jsonify({
        'success': True,
        'message': '💧 Hydration logged! +15 XP earned.',
        'profile': profile
    })

@app.route('/api/focus/complete', methods=['POST'])
def complete_focus():
    data = request.get_json() or {}
    minutes = int(data.get('minutes', 15))
    earned_xp = data_manager.log_focus_session(minutes)
    profile = data_manager.get_user_profile()
    return jsonify({
        'success': True,
        'message': f'🎉 Focus session ({minutes} mins) completed! +{earned_xp} Focus XP awarded!',
        'earned_xp': earned_xp,
        'profile': profile
    })

@app.route('/api/quests/claim', methods=['POST'])
def claim_quest():
    data = request.get_json() or {}
    quest_id = data.get('quest_id')
    awarded = data_manager.complete_daily_quest(quest_id)
    profile = data_manager.get_user_profile()
    return jsonify({
        'success': awarded > 0,
        'awarded_xp': awarded,
        'profile': profile
    })

# =========================================================
# WORKOUT TRACKER & STREAK APIS
# =========================================================

@app.route('/api/workout/log', methods=['POST'])
@app.route('/api/workout/claim', methods=['POST'])
def log_workout_endpoint():
    data = request.get_json() or {}
    name = data.get('workout_name') or data.get('name') or 'Dorm Movement Session'
    w_type = data.get('workout_type', 'Strength')
    duration = data.get('duration', '10 Mins')
    equipment = data.get('equipment', 'Bodyweight')
    intensity = data.get('intensity', 'Moderate Strength')
    calories = int(data.get('calories', 60))
    xp = int(data.get('xp', 35))

    stats = data_manager.log_workout(
        workout_name=name,
        workout_type=w_type,
        duration=duration,
        equipment=equipment,
        intensity=intensity,
        calories=calories,
        xp=xp
    )
    logs = data_manager.get_workout_logs(limit=20)
    profile = data_manager.get_user_profile()

    streak_val = stats.get('streak', 1)
    return jsonify({
        'success': True,
        'message': f'💪 "{name}" recorded! +{xp} Movement XP awarded! Streak: {streak_val} days 🔥',
        'stats': stats,
        'logs': logs,
        'profile': profile
    })

@app.route('/api/workout/history', methods=['GET'])
def get_workout_history():
    logs = data_manager.get_workout_logs(limit=30)
    stats = data_manager.get_workout_stats()
    return jsonify({
        'success': True,
        'logs': logs,
        'stats': stats
    })

@app.route('/api/workout/<int:log_id>', methods=['DELETE'])
def delete_workout_endpoint(log_id):
    stats = data_manager.delete_workout_log(log_id)
    logs = data_manager.get_workout_logs(limit=20)
    profile = data_manager.get_user_profile()
    return jsonify({
        'success': True,
        'message': 'Workout log removed.',
        'stats': stats,
        'logs': logs,
        'profile': profile
    })

# =========================================================
# LITERARY CORNER APIS
# =========================================================

@app.route('/api/literary', methods=['POST'])
def create_literary_post():
    author = request.form.get('author') or (request.json.get('author') if request.is_json else None) or 'Anonymous Writer'
    title = request.form.get('title') or (request.json.get('title') if request.is_json else None) or 'Untitled Reflection'
    content = request.form.get('content') or (request.json.get('content') if request.is_json else None) or ''
    tag = request.form.get('tag') or (request.json.get('tag') if request.is_json else None) or 'Student Voice'

    if not content.strip():
        return jsonify({'success': False, 'message': 'Content cannot be empty.'}), 400

    data_manager.add_literary_post(author.strip(), title.strip(), content.strip(), tag)
    posts = data_manager.get_literary_posts()
    profile = data_manager.get_user_profile()

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'posts': posts, 'profile': profile})
    
    return index()

@app.route('/api/literary/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    new_likes = data_manager.like_literary_post(post_id)
    profile = data_manager.get_user_profile()
    return jsonify({
        'success': True,
        'likes': new_likes,
        'profile': profile
    })

# =========================================================
# DOODLE STUDIO & GALLERY APIS
# =========================================================

@app.route('/api/doodles', methods=['GET', 'POST'])
def handle_doodles():
    if request.method == 'POST':
        data = request.get_json() or {}
        author = data.get('author', 'Anonymous Artist')
        title = data.get('title', 'Dorm Canvas Sketch')
        image_data = data.get('image_data', '')
        if not image_data:
            return jsonify({'success': False, 'message': 'Canvas data is empty.'}), 400
        new_id = data_manager.save_doodle(author, title, image_data)
        doodles = data_manager.get_doodles(limit=30)
        profile = data_manager.get_user_profile()
        return jsonify({
            'success': True,
            'id': new_id,
            'message': '🎨 Doodle saved to your gallery! +25 XP awarded!',
            'doodles': doodles,
            'profile': profile
        })
    else:
        doodles = data_manager.get_doodles(limit=30)
        return jsonify({'success': True, 'doodles': doodles})

@app.route('/api/doodles/<int:doodle_id>', methods=['GET'])
def get_single_doodle(doodle_id):
    doodle = data_manager.get_doodle_by_id(doodle_id)
    if not doodle:
        return jsonify({'success': False, 'message': 'Doodle not found.'}), 404
    return jsonify({'success': True, 'doodle': doodle})

@app.route('/api/doodles/<int:doodle_id>', methods=['DELETE'])
def delete_single_doodle(doodle_id):
    data_manager.delete_doodle(doodle_id)
    doodles = data_manager.get_doodles(limit=30)
    profile = data_manager.get_user_profile()
    return jsonify({
        'success': True,
        'message': 'Doodle deleted from gallery.',
        'doodles': doodles,
        'profile': profile
    })

# =========================================================
# READING PROGRESS & BOOKMARK APIS
# =========================================================

@app.route('/api/reading/progress', methods=['POST'])
def update_reading_progress():
    data = request.get_json() or {}
    book_id = data.get('book_id', 'alice')
    page_num = int(data.get('page_num', 1))

    data_manager.save_reading_progress(book_id, page_num)
    progress = data_manager.get_reading_progress(book_id)
    profile = data_manager.get_user_profile()

    return jsonify({
        'success': True,
        'message': f'📖 Page {page_num} saved! +10 Reading XP',
        'progress': progress,
        'profile': profile
    })

@app.route('/api/reading/progress/<book_id>', methods=['GET'])
def fetch_reading_progress(book_id):
    progress = data_manager.get_reading_progress(book_id)
    return jsonify({'success': True, 'progress': progress})

# Dynamic Speed Math Challenge API
@app.route('/api/puzzle/math', methods=['GET'])
def get_math_puzzle():
    ops = ['+', '-', '*']
    op = random.choice(ops)
    if op == '+':
        a = random.randint(15, 85)
        b = random.randint(12, 68)
        ans = a + b
    elif op == '-':
        a = random.randint(35, 120)
        b = random.randint(10, a - 5)
        ans = a - b
    else:
        a = random.randint(6, 15)
        b = random.randint(4, 12)
        ans = a * b

    return jsonify({
        'question': f"{a} {op} {b}",
        'id': f"{a}_{op}_{b}"
    })

@app.route('/api/puzzle/math/verify', methods=['POST'])
def verify_math_puzzle():
    data = request.get_json() or {}
    puzzle_id = data.get('id', '')
    user_ans = data.get('answer', '')

    try:
        parts = puzzle_id.split('_')
        a, op, b = int(parts[0]), parts[1], int(parts[2])
        if op == '+': correct = a + b
        elif op == '-': correct = a - b
        else: correct = a * b

        is_correct = int(user_ans) == correct
        earned_xp = 20 if is_correct else 0
        if is_correct:
            profile = data_manager.update_user_profile(xp_add=20)
        else:
            profile = data_manager.get_user_profile()

        return jsonify({
            'correct': is_correct,
            'expected': correct,
            'earned_xp': earned_xp,
            'profile': profile
        })
    except Exception as e:
        return jsonify({'correct': False, 'error': str(e)}), 400

# Riddles API
@app.route('/api/puzzle/riddle', methods=['GET'])
def get_riddle():
    riddle = random.choice(data_manager.RIDDLES_BANK)
    return jsonify({
        'id': riddle['id'],
        'riddle': riddle['riddle'],
        'hint': riddle['hint']
    })

@app.route('/api/puzzle/riddle/verify', methods=['POST'])
def verify_riddle():
    data = request.get_json() or {}
    riddle_id = int(data.get('id', 1))
    guess = str(data.get('guess', '')).lower().strip()

    target = None
    for r in data_manager.RIDDLES_BANK:
        if r['id'] == riddle_id:
            target = r
            break

    if not target:
        return jsonify({'correct': False, 'message': 'Riddle not found'}), 404

    is_correct = target['answer'] in guess or guess in target['answer']
    earned_xp = 25 if is_correct else 0
    if is_correct:
        profile = data_manager.update_user_profile(xp_add=25)
    else:
        profile = data_manager.get_user_profile()

    return jsonify({
        'correct': is_correct,
        'answer': target['answer'],
        'earned_xp': earned_xp,
        'profile': profile
    })

# Export History as CSV
@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    history = data_manager.get_history_logs(limit=100)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Timestamp', 'Sleep (hrs)', 'Screen (hrs)', 'Stress (1-10)', 'Mood', 'Transport Mode', 'Distance (km)', 'Diet', 'CO2 (kg)', 'Burnout Level', 'XP Earned'])
    
    for h in history:
        writer.writerow([
            h['id'], h['timestamp'], h['sleep'], h['screen'], h['stress'], h['mood'],
            h['transport'], h['distance'], h['diet'], h['co2'], h['burnout'], h['xp_earned']
        ])

    csv_data = output.getvalue()
    response = make_response(csv_data)
    response.headers['Content-Disposition'] = 'attachment; filename=ecopulse_activity_history.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

def find_available_port(preferred_port=5050):
    """Finds an open port starting from preferred_port."""
    import socket
    port = preferred_port
    while port < 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            port += 1
    return preferred_port

if __name__ == '__main__':
    import os
    target_port = int(os.environ.get('PORT', 5050))
    chosen_port = find_available_port(target_port)

    print("🌱 EcoPulse Master Platform launching...")
    print("Developed with pride for Team Invicta Chaos (Sneha, Aditi, Divyanshi & Panchmi)")
    print(f"🚀 Server running at: http://localhost:{chosen_port} (and http://127.0.0.1:{chosen_port})")
    app.run(host='0.0.0.0', port=chosen_port, debug=True)
