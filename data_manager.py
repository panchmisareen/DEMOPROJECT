import sqlite3
import os
import json
import datetime
import random

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ecopulse.db')

DEFAULT_QUOTES = [
    {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain", "category": "Action"},
    {"quote": "Small daily improvements over time lead to stunning results.", "author": "Robin Sharma", "category": "Habits"},
    {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "category": "Resilience"},
    {"quote": "Caring for yourself is caring for the planet. Every mindful choice echoes outward.", "author": "EcoPulse", "category": "Eco-Mindset"},
    {"quote": "You don’t have to be great to start, but you have to start to be great.", "author": "Zig Ziglar", "category": "Motivation"},
    {"quote": "Rest when you’re weary. Refresh and renew yourself, your body, your mind.", "author": "Mindfulness Guide", "category": "Wellness"},
    {"quote": "The greatest threat to our planet is the belief that someone else will save it.", "author": "Robert Swan", "category": "Climate Action"},
    {"quote": "Almost everything will work again if you unplug it for a few minutes, including you.", "author": "Anne Lamott", "category": "Digital Detox"},
    {"quote": "Study hard, breathe deep, step lightly on the Earth.", "author": "Campus Mindfulness", "category": "Campus Life"}
]

DEFAULT_BOOKS = [
    {
        "id": "alice",
        "title": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "genre": "Fantasy / Classic",
        "read_time": "15 mins",
        "pages": [
            {
                "page_num": 1,
                "title": "Chapter I: Down the Rabbit-Hole (Part 1)",
                "text": """CHAPTER I. Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.

There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!' but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT-POCKET, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it..."""
            },
            {
                "page_num": 2,
                "title": "Chapter I: Down the Rabbit-Hole (Part 2)",
                "text": """...and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.

In another moment down went Alice after it, never once considering how in the world she was to get out again.

The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.

Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs.

She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it.

'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs!'"""
            },
            {
                "page_num": 3,
                "title": "Chapter II: The Pool of Tears",
                "text": """CHAPTER II. The Pool of Tears

'Curiouser and curiouser!' cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); 'now I'm opening out like the largest telescope that ever was! Good-bye, feet!' (for when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off). 'Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I'm sure I shan't be able! I shall be a great deal too far off to trouble myself about you: you must manage the best way you can;—but I must be kind to them,' thought Alice, 'or perhaps they won't walk the way I want to go! Let me see: I'll give them a new pair of boots every Christmas.'

And she went on planning to herself how she would manage it. 'They must go by the carrier,' she thought; 'and how funny it'll seem, sending presents to one's own feet! And how odd the directions will look!

    Alice's Right Foot, Esq.
    Hearthrug,
    near the Fender,
    (with Alice's love).

Oh dear, what nonsense I'm talking!' Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried off to the garden door."""
            }
        ]
    },
    {
        "id": "walden",
        "title": "Walden; or, Life in the Woods",
        "author": "Henry David Thoreau",
        "genre": "Nature & Philosophy",
        "read_time": "15 mins",
        "pages": [
            {
                "page_num": 1,
                "title": "Chapter II: Where I Lived, and What I Lived For (Part 1)",
                "text": """CHAPTER II. Where I Lived, and What I Lived For

When first I took up my abode in the woods, that is, began to spend my nights as well as days there, which, by accident, was on Independence Day, or the Fourth of July, 1845, my house was not finished for winter, but was merely a defence against the rain, without plastering or chimney, the walls being of rough weather-stained boards, with wide chinks, which made it cool at night.

The upright white hewn studs and freshly planed door and window casings gave it a clean and airy look, especially in the morning, when its timbers were saturated with dew. To my imagination it retained throughout the day more or less of this auroral character.

Every morning was a cheerful invitation to make my life of equal simplicity, and I may say innocence, with Nature herself. I have been as sincere a worshipper of Aurora as the Greeks. I got up early and bathed in the pond; that was a religious exercise, and one of the best things which I did."""
            },
            {
                "page_num": 2,
                "title": "Chapter II: Where I Lived, and What I Lived For (Part 2)",
                "text": """I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived. I did not wish to live what was not life, living is so dear; nor did I wish to practise resignation, unless it was quite necessary.

I wanted to live deep and suck out all the marrow of life, to live so sturdily and Spartan-like as to put to rout all that was not life, to cut a broad swath and shave close, to drive life into a corner, and reduce it to its lowest terms.

Our life is frittered away by detail. An honest man has hardly need to count more than his ten fingers, or in extreme cases he may add his ten toes, and lump the rest. Simplicity, simplicity, simplicity! I say, let your affairs be as two or three, and not a hundred or a thousand; instead of a million count half a dozen, and keep your accounts on your thumb-nail."""
            },
            {
                "page_num": 3,
                "title": "Chapter V: Solitude & Serenity",
                "text": """CHAPTER V. Solitude

This is a delicious evening, when the whole body is one sense, and imbibes delight through every pore. I go and come with a strange liberty in Nature, a part of herself. As I walk along the stony shore of the pond in my shirt-sleeves, though it is cool as well as cloudy and windy, and I see nothing special to attract me, all the elements are unusually congenial to me.

The bullfrogs trump to usher in the night, and the note of the whip-poor-will is borne on the rippling wind from over the water. Sympathy with the fluttering alder and poplar leaves almost takes away my breath; yet, like the lake, my serenity is rippled but not ruffled.

There can be no very black melancholy to him who lives in the midst of nature and has his senses still. There was never yet such a storm but it was Æolian music to a healthy and innocent ear. Nothing can rightly compel a simple and brave man to a vulgar sadness."""
            }
        ]
    },
    {
        "id": "meditations",
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "genre": "Stoicism & Mental Balance",
        "read_time": "12 mins",
        "pages": [
            {
                "page_num": 1,
                "title": "Book IV: The Inner Sanctuary",
                "text": """BOOK IV. Inner Sanctuary & Serenity

Men look for retreats for themselves, the country, the sea-shore, the hills; and you yourself, too, are peculiarly accustomed to long for such things. But the whole matter is in the highest degree unphilosophical, since you can at any time you wish retire into yourself.

For nowhere can a man find a quieter or more untroubled retreat than in his own soul, above all when he possesses within himself such features that in looking into them he straightway enjoys total serenity. And by serenity I mean nothing other than the proper ordering of the mind.

Constantly then grant yourself this retreat, and renew yourself. Let your principles be brief and fundamental, which as soon as you recur to them will be sufficient to cleanse all sorrow and send you back without irritation to the duties to which you return."""
            },
            {
                "page_num": 2,
                "title": "Book IV: Transience and Peace",
                "text": """Remember that all things are sphere-like and cyclical, and that it is of no consequence whether a man sees the same things for a hundred years or two hundred or for an eternity.

Observe how transient and trivial are all mortal things: yesterday a drop of semen, tomorrow a handful of ash or mummy. Pass then through this little space of time conforming to nature, and end your journey in contentment, just as an olive falls off when it is ripe, blessing nature who produced it, and thanking the tree on which it grew.

Be like the promontory against which the waves continually break, but it stands firm and tames the fury of the water around it. 'Unhappy am I, because this has happened to me.' Not so, but: 'Happy am I, though this has happened to me, because I continue free from pain, neither crushed by the present nor fearing the future.'"""
            },
            {
                "page_num": 3,
                "title": "Book IV: Universal Harmony",
                "text": """Everything harmonizes with me, which is harmonious to thee, O Universe. Nothing for me is too early nor too late, which is in due time for thee. Everything is fruit to me which thy seasons bring, O Nature: from thee are all things, in thee are all things, to thee all things return.

Doth any man dread change? What can take place without change? What then is more pleasing or more suitable to universal nature? And canst thou take a bath unless the wood undergoes a change? And canst thou be nourished unless the food undergoes a change? And can anything else that is useful be accomplished without change?

Do not act as if you had ten thousand years to throw away. Death stands at your elbow. Here and now, while you are alive and have it in your power, be good."""
            }
        ]
    },
    {
        "id": "artofwar",
        "title": "The Art of War",
        "author": "Sun Tzu",
        "genre": "Strategy & Focus",
        "read_time": "10 mins",
        "pages": [
            {
                "page_num": 1,
                "title": "Chapter I: Laying Plans",
                "text": """CHAPTER I. Laying Plans

1. Sun Tzu said: The art of war is of vital importance to the State.
2. It is a matter of life and death, a road either to safety or to ruin. Hence it is a subject of inquiry which can on no account be neglected.
3. The art of war, then, is governed by five constant factors: (1) The Moral Law; (2) Heaven; (3) Earth; (4) The Commander; (5) Method and discipline.

The Moral Law causes the people to be in complete accord with their ruler, so that they will follow him regardless of their lives, undismayed by any danger.

Heaven signifies night and day, cold and heat, times and seasons. Earth comprises distances, great and small; danger and security; open ground and narrow passes; the chances of life and death."""
            },
            {
                "page_num": 2,
                "title": "Chapter II: Waging War & Conservation",
                "text": """CHAPTER II. Waging War

1. In the operations of war, where there are in the field a thousand swift chariots, as many heavy chariots, and a hundred thousand mail-clad soldiers, with provisions enough to carry them a thousand li, the expenditure at home and at the front will reach the total of a thousand ounces of silver per day. Such is the cost of raising an army.

2. When you engage in actual fighting, if victory is long in coming, then men's weapons will grow dull and their ardor will be damped. If you lay siege to a town, you will exhaust your strength.

3. Now, when your weapons are dulled, your ardor damped, your strength exhausted and your treasure spent, other chieftains will spring up to take advantage of your extremity. Then no man, however wise, will be able to avert the consequences that must ensue.

4. Thus, though we have heard of stupid haste in war, cleverness has never been seen associated with long delays. There is no instance of a country having benefited from prolonged warfare."""
            },
            {
                "page_num": 3,
                "title": "Chapter III: Attack by Stratagem",
                "text": """CHAPTER III. Attack by Stratagem

1. Sun Tzu said: In the practical art of war, the best thing of all is to take the enemy's country whole and intact; to shatter and destroy it is not so good. So, too, it is better to recapture an army entire than to destroy it.

2. Hence to fight and conquer in all your battles is not supreme excellence; supreme excellence consists in breaking the enemy's resistance without fighting.

3. Thus the highest form of generalship is to balk the enemy's plans; the next best is to prevent the junction of the enemy's forces; the next in order is to attack the enemy's army in the field; and the worst policy of all is to besiege walled cities.

4. If you know the enemy and know yourself, you need not fear the result of a hundred battles. If you know yourself but not the enemy, for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself, you will succumb in every battle."""
            }
        ]
    },
    {
        "id": "sherlock",
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "genre": "Mystery & Deduction",
        "read_time": "12 mins",
        "pages": [
            {
                "page_num": 1,
                "title": "Adventure I: A Scandal in Bohemia (Part 1)",
                "text": """ADVENTURE I. A SCANDAL IN BOHEMIA

To Sherlock Holmes she is always THE woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind. He was, I take it, the most perfect reasoning and observing machine that the world has seen.

I had seen little of Holmes lately. My marriage had drifted us away from each other. My own complete happiness, and the home-centred interests which rise up around the man who first finds himself master of his own establishment, were sufficient to absorb all my attention; while Holmes, who loathed every form of society with his whole Bohemian soul, remained in our lodgings in Baker Street, alternating from week to week between cocaine and ambition, the drowsiness of the drug, and the fierce energy of his own keen nature."""
            },
            {
                "page_num": 2,
                "title": "Adventure I: A Scandal in Bohemia (Part 2)",
                "text": """One night—it was on the twentieth of March, 1888—I was returning from a journey to a patient (for I had now returned to civil practice), when my way led me through Baker Street. As I passed the well-remembered door, which must always be associated in my mind with my wooing, and with the dark incidents of the Study in Scarlet, I was seized with a keen desire to see Holmes again, and to know how he was employing his extraordinary powers.

His rooms were brilliantly lit, and, even as I looked up, I saw his tall, spare figure pass twice in a dark silhouette against the blind. He was pacing the room swiftly, eagerly, with his head sunk upon his chest and his hands clasped behind him. To me, who knew his every mood and habit, his attitude and manner told their own story. He was at work again. He had risen out of his drug-created dreams and was hot upon the scent of some new problem.

I rang the bell and was shown up to the chamber which had formerly been in part my own."""
            },
            {
                "page_num": 3,
                "title": "Adventure I: A Scandal in Bohemia (Part 3)",
                "text": """His manner was not effusive. It seldom was; but he was glad, I think, to see me. With hardly a word spoken, but with a kindly eye, he waved me to an armchair, threw across his case of cigars, and indicated an alcove where stood a tantalus and a siphon. Then he stood before the fire and looked me over in his singular introspective fashion.

'Wedlock suits you,' he remarked. 'I think, Watson, that you have put on seven and a half pounds since I saw you.'

'Seven!' I answered.

'Indeed, I should have thought a little more. Just a trifle more, I fancy, Watson. And in practice again, I observe. You did not tell me that you intended to go into harness.'

'Then, how do you know?'

'I see it, I deduce it. How do I know that you have been getting yourself very wet lately, and that you have a most clumsy and careless servant girl?'

'My dear Holmes,' said I, 'this is too much. You would certainly have been burned, had you lived a few centuries ago. It is quite true that I had a country walk on Thursday and came home in a dreadful mess, but as I have changed my clothes I can't imagine how you deduce it.'

He chuckled to himself and rubbed his long, nervous hands together. 'It is simplicity itself,' said he."""
            }
        ]
    }
]

DEFAULT_RECIPES = [
    {
        "id": "avocado-toast",
        "title": "🥑 Avocado & Crispy Chickpea Power Toast",
        "category": "Quick Dorm (<5 mins)",
        "time": "5 mins",
        "co2": "0.38 kg CO₂ (Saves 3.1 kg vs Bacon & Egg Bagel)",
        "calories": "320 kcal",
        "protein": "14g Protein",
        "cost": "Low (~$1.50)",
        "tags": ["Vegan", "High Fiber", "Brain Boost"],
        "ingredients": [
            "1 slice 100% whole grain sourdough or seeded bread",
            "1/2 ripe avocado mashed with lime juice",
            "1/2 cup canned seasoned chickpeas (rinsed & drained)",
            "Pinch of sea salt, black pepper & smoked paprika",
            "1 tsp hemp seeds or toasted sesame"
        ],
        "instructions": "Toast bread till golden crisp. Mash avocado directly on top with lime and seasonings. Pile high with chickpeas and sprinkle hemp seeds for healthy omega-3 fats!"
    },
    {
        "id": "berry-smoothie",
        "title": "🫐 Midnight Study Antioxidant Berry Bowl",
        "category": "Brain Recharge",
        "time": "3 mins",
        "co2": "0.29 kg CO₂ (Saves 3.3 kg vs Dairy Milkshake)",
        "calories": "270 kcal",
        "protein": "11g Protein",
        "cost": "Budget-Friendly",
        "tags": ["No Stove", "Eye Health", "Antioxidants"],
        "ingredients": [
            "1 cup frozen wild blueberries and strawberries",
            "1 frozen ripe banana (natural sweetener)",
            "1/2 cup unsweetened oat or almond milk",
            "1 scoop plant protein or 1 tbsp chia seeds",
            "Handful of granola and pumpkin seeds on top"
        ],
        "instructions": "Blend berries, banana, and plant milk until thick and creamy. Pour into your favorite dorm mug, top with crunchy seeds and granola. Instant brain stamina!"
    },
    {
        "id": "black-bean-burrito",
        "title": "🌮 4-Min Dorm Black Bean & Guac Burrito",
        "category": "Hearty Meal",
        "time": "4 mins",
        "co2": "0.45 kg CO₂ (Saves 3.2 kg vs Beef Burrito)",
        "calories": "410 kcal",
        "protein": "19g Protein",
        "cost": "Low (~$2.00)",
        "tags": ["High Protein", "Quick Prep", "Energy Dense"],
        "ingredients": [
            "1 large whole wheat tortilla wrap",
            "1/2 cup canned black beans (warmed 40s in microwave)",
            "2 tbsp fresh tomato salsa",
            "Handful of baby spinach or cilantro",
            "2 tbsp corn kernels & splash of hot sauce"
        ],
        "instructions": "Layer warm black beans, salsa, spinach, and corn onto the wrap. Roll tightly, slice in half diagonally. Zero pans to wash!"
    },
    {
        "id": "peanut-butter-energy-bites",
        "title": "🥜 No-Bake Oatmeal Peanut Butter Energy Bites",
        "category": "Study Snacks",
        "time": "5 mins",
        "co2": "0.22 kg CO₂ (Saves 2.8 kg vs Processed Candy Bars)",
        "calories": "190 kcal (2 bites)",
        "protein": "7g Protein",
        "cost": "Ultra Cheap",
        "tags": ["No-Cook", "Study Fuel", "Prep Ahead"],
        "ingredients": [
            "1 cup rolled oats",
            "1/3 cup natural peanut butter",
            "2 tbsp maple syrup or honey",
            "1 tbsp dark chocolate chips",
            "1 tbsp flaxseed meal"
        ],
        "instructions": "Stir ingredients in a bowl until dough forms. Roll into 8 small bite-sized balls and store in a jar or mini fridge. Perfect 3 PM study pick-me-up!"
    }
]

DEFAULT_WORKOUTS = {
    'High': [
        {
            "id": "w1",
            "name": "5-Min Dorm Deep Breathing & Neck Relief",
            "type": "Restorative",
            "duration": "5 Mins",
            "equipment": "None (Bed / Chair)",
            "intensity": "High Fatigue / Restorative",
            "calories": 25,
            "desc": "Sit tall with feet flat. Inhale 4s, hold 4s, exhale 6s. Rotate neck gently clockwise then counter-clockwise. Releases screen tension immediately."
        },
        {
            "id": "w2",
            "name": "Gentle Seated Hamstring & Spinal Twist",
            "type": "Flexibility",
            "duration": "7 Mins",
            "equipment": "Chair / Bed",
            "intensity": "High Fatigue / Restorative",
            "calories": 35,
            "desc": "Extend legs forward and hinge at hips. Hold for 30s. Cross right leg over left and gently twist torso. Calms nervous system."
        },
        {
            "id": "w3",
            "name": "Legs-Up-The-Wall Deep Relaxation",
            "type": "Mindfulness & Blood Flow",
            "duration": "8 Mins",
            "equipment": "Dorm Wall",
            "intensity": "High Fatigue / Restorative",
            "calories": 20,
            "desc": "Lie flat on your rug and prop your legs vertically up against the wall. Closes lymphatic loop, reduces headache pressure and foot soreness."
        }
    ],
    'Moderate': [
        {
            "id": "w4",
            "name": "Silent Dorm Wall Sits & Arm Reach",
            "type": "Lower Body Strength",
            "duration": "3 Sets x 35s",
            "equipment": "Dorm Wall",
            "intensity": "Moderate Strength",
            "calories": 65,
            "desc": "Slide down against a flat wall until thighs are parallel to rug. Hold steady while maintaining calm diaphragmatic breathing. Completely silent for roommates."
        },
        {
            "id": "w5",
            "name": "Rug Glute Bridges & Isometric Hold",
            "type": "Posterior Chain",
            "duration": "3 Sets x 15 Reps",
            "equipment": "Floor / Rug",
            "intensity": "Moderate Strength",
            "calories": 55,
            "desc": "Lie on back with knees bent, feet hip-width apart. Drive through heels to lift hips, squeeze glutes at the top for 2 seconds. Counteracts prolonged sitting."
        },
        {
            "id": "w6",
            "name": "Forearm Plank to Pike",
            "type": "Core & Posture",
            "duration": "3 Sets x 30s",
            "equipment": "Floor / Rug",
            "intensity": "Moderate Strength",
            "calories": 50,
            "desc": "Hold standard forearm plank, then push hips upward into an inverted V (pike), return under control. Builds bulletproof study posture."
        }
    ],
    'Low': [
        {
            "id": "w7",
            "name": "12-Min Full-Body Dorm HIIT Burn",
            "type": "High Energy Cardio",
            "duration": "3 Rounds",
            "equipment": "Bodyweight",
            "intensity": "High Energy HIIT",
            "calories": 130,
            "desc": "Bodyweight air squats, floor push-ups, alternating reverse lunges, and plank shoulder taps. Quick calorie burn and endorphin surge."
        },
        {
            "id": "w8",
            "name": "Core Blast: Bicycle Crunches & Flutter Kicks",
            "type": "Abdominal HIIT",
            "duration": "3 Sets x 40s",
            "equipment": "Floor / Rug",
            "intensity": "High Energy HIIT",
            "calories": 85,
            "desc": "Slow controlled bicycle crunches touching opposite elbow to knee, followed immediately by 20s of flutter kicks. Tightens core and energizes focus."
        },
        {
            "id": "w9",
            "name": "Shadow Boxing & Dynamic High Knees",
            "type": "Cardio Stamina",
            "duration": "4 Rounds x 1 Min",
            "equipment": "Small 2x2m space",
            "intensity": "High Energy HIIT",
            "calories": 110,
            "desc": "30s jab-cross-hook rhythm followed by 30s light springy high knees. Releases pent-up study stress fast."
        }
    ]
}

RIDDLES_BANK = [
    {
        "id": 1,
        "riddle": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "answer": "echo",
        "hint": "Think of sound reverberating back across a valley or empty hall."
    },
    {
        "id": 2,
        "riddle": "The more of this you take, the more you leave behind. What are they?",
        "answer": "footsteps",
        "hint": "Think of walking on campus paths or in the snow."
    },
    {
        "id": 3,
        "riddle": "I absorb carbon by day, provide shade for study, and breathe life into our atmosphere without asking for a thing. What am I?",
        "answer": "tree",
        "hint": "Found in forests, parks, and outside dorm windows."
    },
    {
        "id": 4,
        "riddle": "I have cities, but no houses; forests, but no trees; and water, but no fish. What am I?",
        "answer": "map",
        "hint": "You use me to navigate campuses or cross-country road trips."
    },
    {
        "id": 5,
        "riddle": "What gets wetter and wetter the more it dries?",
        "answer": "towel",
        "hint": "Used in dorm bathrooms after a refreshing shower."
    }
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    c = conn.cursor()

    # User Gamification Profile
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            total_xp INTEGER DEFAULT 250,
            streak_days INTEGER DEFAULT 4,
            bottles_saved INTEGER DEFAULT 18,
            total_co2_saved REAL DEFAULT 21.4,
            glasses_drank_today INTEGER DEFAULT 5,
            workout_streak INTEGER DEFAULT 3,
            level INTEGER DEFAULT 2,
            level_title TEXT DEFAULT 'Green Scholar',
            xp_percent INTEGER DEFAULT 75,
            plant_stage TEXT DEFAULT '🌿 Young Sprout',
            last_active_date TEXT
        )
    ''')

    # Activity History Logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS history_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sleep REAL,
            screen REAL,
            stress INTEGER,
            mood TEXT,
            transport TEXT,
            distance REAL,
            diet TEXT,
            co2 REAL,
            burnout TEXT,
            burnout_class TEXT,
            xp_earned INTEGER
        )
    ''')

    # Literary Corner Posts (no member names)
    c.execute('''
        CREATE TABLE IF NOT EXISTS literary_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            title TEXT,
            content TEXT,
            tag TEXT DEFAULT 'Poetry',
            likes INTEGER DEFAULT 0,
            timestamp TEXT
        )
    ''')

    # Community & Saved Doodles
    c.execute('''
        CREATE TABLE IF NOT EXISTS doodles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            title TEXT,
            image_data TEXT,
            timestamp TEXT
        )
    ''')

    # Workout Activity Logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_name TEXT,
            workout_type TEXT,
            duration TEXT,
            equipment TEXT,
            intensity TEXT,
            calories_est INTEGER,
            xp_earned INTEGER DEFAULT 35,
            date_str TEXT,
            timestamp TEXT
        )
    ''')

    # Reading Bookmarks & Progress
    c.execute('''
        CREATE TABLE IF NOT EXISTS reading_progress (
            book_id TEXT PRIMARY KEY,
            current_page INTEGER DEFAULT 1,
            total_pages INTEGER DEFAULT 3,
            last_read_at TEXT
        )
    ''')

    # Focus Sessions
    c.execute('''
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            minutes INTEGER,
            timestamp TEXT,
            completed INTEGER DEFAULT 1
        )
    ''')

    # Daily Quests
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quest_id TEXT UNIQUE,
            title TEXT,
            target INTEGER,
            current INTEGER DEFAULT 0,
            xp_reward INTEGER,
            completed INTEGER DEFAULT 0,
            date_str TEXT
        )
    ''')

    # Badges
    c.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_id TEXT UNIQUE,
            title TEXT,
            description TEXT,
            icon TEXT,
            unlocked INTEGER DEFAULT 0,
            unlocked_at TEXT
        )
    ''')

    conn.commit()

    # Clean existing member names from literary_posts table (replace with student pseudonyms)
    name_replacements = {
        'Sneha K.': 'EcoScholar',
        'Aditi J.': 'MidnightPoet',
        'Divyanshi D.': 'AutumnDreamer',
        'Panchmi S.': 'SolarWanderer'
    }
    for old_name, new_name in name_replacements.items():
        c.execute('UPDATE literary_posts SET author = ? WHERE author LIKE ?', (new_name, f"%{old_name}%"))

    # Seed User Profile if empty
    c.execute('SELECT COUNT(*) FROM user_profile')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO user_profile (id, total_xp, streak_days, bottles_saved, total_co2_saved, glasses_drank_today, workout_streak, level, level_title, xp_percent, plant_stage, last_active_date)
            VALUES (1, 260, 4, 18, 22.4, 5, 3, 2, 'Green Scholar', 80, '🌿 Vibrant Young Sprout', ?)
        ''', (datetime.date.today().isoformat(),))

    # Seed Literary Posts if empty
    c.execute('SELECT COUNT(*) FROM literary_posts')
    if c.fetchone()[0] == 0:
        seed_posts = [
            ("EcoScholar", "Ode to the Campus Oak", "Standing tall against the breeze, breathing life into the trees; roots anchored deep below the stone, a sanctuary when I'm alone.", "Nature & Eco", 14, "Yesterday at 6:40 PM"),
            ("MidnightPoet", "Midnight Code & Starlight", "Lines of logic, dreams untamed, in quiet corridors reclaimed. A syntax sweet, a mind ignited, where tech and human heart are united.", "Campus Life", 19, "Yesterday at 11:15 PM"),
            ("AutumnDreamer", "Whispers of Autumn Dew", "Golden leaves on gravel paths, leaving stress in yesterday's drafts. Inhale the breeze of crisp cold dawn, another mindful day is born.", "Mindfulness", 12, "Today at 8:20 AM"),
            ("SolarWanderer", "Cycle Commute Serenade", "Pedals spinning, gears in sync, cooler thoughts before I think. Zero smoke behind my trail, green horizon will prevail.", "Nature & Eco", 22, "Today at 9:05 AM")
        ]
        c.executemany('''
            INSERT INTO literary_posts (author, title, content, tag, likes, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_posts)

    # Seed Workout Logs if empty
    c.execute('SELECT COUNT(*) FROM workout_logs')
    if c.fetchone()[0] == 0:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        two_days_ago = today - datetime.timedelta(days=2)
        initial_workouts = [
            ("5-Min Dorm Deep Breathing & Neck Relief", "Restorative", "5 Mins", "None (Bed / Chair)", "High Fatigue / Restorative", 25, 35, today.isoformat(), "Today at 07:45 AM"),
            ("Silent Dorm Wall Sits & Arm Reach", "Lower Body Strength", "3 Sets x 35s", "Dorm Wall", "Moderate Strength", 65, 35, yesterday.isoformat(), "Yesterday at 05:30 PM"),
            ("12-Min Full-Body Dorm HIIT Burn", "High Energy Cardio", "3 Rounds", "Bodyweight", "High Energy HIIT", 130, 35, two_days_ago.isoformat(), "2 days ago at 06:15 PM")
        ]
        c.executemany('''
            INSERT INTO workout_logs (workout_name, workout_type, duration, equipment, intensity, calories_est, xp_earned, date_str, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_workouts)

    # Seed Badges if empty
    c.execute('SELECT COUNT(*) FROM badges')
    if c.fetchone()[0] == 0:
        badges_list = [
            ("first_diagnostic", "Eco Pioneer", "Completed your first EcoPulse comprehensive diagnostic", "🌱", 1, "2026-10-22"),
            ("zero_emission", "Carbon Neutral Voyager", "Chose walking or cycling for campus commute", "🚲", 1, "2026-10-23"),
            ("hydration_hero", "Hydration Sentinel", "Logged 8+ glasses of fresh water in a day", "💧", 0, None),
            ("workout_warrior", "Movement Champion", "Maintained an active dorm fitness streak", "🏋️", 1, "2026-10-24"),
            ("zen_master", "Mindful Breathing Master", "Completed a full 5-minute Zen breathing cycle", "🧘", 1, "2026-10-24"),
            ("literary_bard", "Campus Literary Bard", "Published an original poem or reflection in the Corner", "✍️", 1, "2026-10-24"),
            ("deep_focus", "Digital Detox Champion", "Completed a 25-minute deep focus lock session", "🔒", 0, None)
        ]
        c.executemany('''
            INSERT INTO badges (badge_id, title, description, icon, unlocked, unlocked_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', badges_list)

    # Seed History Logs if empty
    c.execute('SELECT COUNT(*) FROM history_logs')
    if c.fetchone()[0] == 0:
        initial_history = [
            ("Today at 10:30 AM", 7.5, 6.0, 3, "Focused", "Bike Walk", 4.0, "Vegetarian", 0.8, "Low", "low", 80),
            ("Yesterday at 04:15 PM", 6.0, 8.5, 6, "Fatigued", "Bus", 6.5, "Balanced", 2.32, "Moderate", "moderate", 60),
            ("Oct 22 at 08:50 PM", 5.5, 9.5, 8, "Anxious", "Car", 5.0, "Meat", 4.55, "High", "high", 50)
        ]
        c.executemany('''
            INSERT INTO history_logs (timestamp, sleep, screen, stress, mood, transport, distance, diet, co2, burnout, burnout_class, xp_earned)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_history)

    # Seed Reading Progress if empty
    for b in DEFAULT_BOOKS:
        c.execute('INSERT OR IGNORE INTO reading_progress (book_id, current_page, total_pages, last_read_at) VALUES (?, 1, ?, ?)',
                  (b['id'], len(b['pages']), datetime.date.today().isoformat()))

    ensure_daily_quests(c)
    conn.commit()
    conn.close()

def ensure_daily_quests(cursor=None):
    today = datetime.date.today().isoformat()
    needs_close = False
    if cursor is None:
        conn = get_db()
        cursor = conn.cursor()
        needs_close = True

    cursor.execute('SELECT COUNT(*) FROM daily_quests WHERE date_str = ?', (today,))
    count = cursor.fetchone()[0]
    if count == 0:
        quests = [
            ("drink_water_8", "Drink 8 glasses of water (Hydration boost)", 8, 5, 30, today),
            ("active_commute", "Choose zero-emission commute (Walk/Cycle)", 1, 1, 40, today),
            ("plant_meal", "Choose a delicious plant-based lunch or dinner", 1, 1, 35, today),
            ("workout_session", "Complete and log any dorm workout routine", 1, 1, 35, today),
            ("focus_lock", "Complete at least 15 mins of Deep Focus Lock", 15, 0, 50, today)
        ]
        cursor.executemany('''
            INSERT OR REPLACE INTO daily_quests (quest_id, title, target, current, xp_reward, completed, date_str)
            VALUES (?, ?, ?, ?, ?, 0, ?)
        ''', [(q[0], q[1], q[2], q[3], q[4], q[5]) for q in quests])

    if needs_close:
        conn.commit()
        conn.close()

def calculate_level_info(total_xp):
    if total_xp >= 800:
        return 5, "Gaia Champion & Guardian", 100, "🌸 Ancient Sacred Guardian Tree"
    elif total_xp >= 500:
        return 4, "Campus Planet Defender", int(((total_xp - 500) / 300) * 100), "🌳 Lush Blooming Tree"
    elif total_xp >= 300:
        return 3, "Mindful Eco-Warrior", int(((total_xp - 300) / 200) * 100), "🪴 Thriving Flowering Pot"
    elif total_xp >= 100:
        return 2, "Green Scholar", int(((total_xp - 100) / 200) * 100), "🌿 Vibrant Young Sprout"
    else:
        return 1, "Eco Novice", int((total_xp / 100) * 100), "🌱 Tender Seedling"

def get_user_profile():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM user_profile WHERE id = 1')
    row = c.fetchone()
    conn.close()
    if row:
        data = dict(row)
        level, title, xp_pct, plant_stage = calculate_level_info(data['total_xp'])
        data['level'] = level
        data['level_title'] = title
        data['xp_percent'] = xp_pct
        data['plant_stage'] = plant_stage
        
        # Calculate dynamic workout streak
        w_stats = get_workout_stats()
        data['workout_streak'] = w_stats['streak']
        data['total_workouts'] = w_stats['total_workouts']
        return data
    return {}

def update_user_profile(xp_add=0, bottles_add=0, co2_saved_add=0.0, water_add=0):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT total_xp, bottles_saved, total_co2_saved, glasses_drank_today FROM user_profile WHERE id = 1')
    row = c.fetchone()
    if row:
        new_xp = max(0, row['total_xp'] + xp_add)
        new_bottles = max(0, row['bottles_saved'] + bottles_add)
        new_co2 = round(max(0.0, row['total_co2_saved'] + co2_saved_add), 2)
        new_water = max(0, row['glasses_drank_today'] + water_add)
        level, title, xp_pct, plant_stage = calculate_level_info(new_xp)

        c.execute('''
            UPDATE user_profile 
            SET total_xp = ?, bottles_saved = ?, total_co2_saved = ?, glasses_drank_today = ?,
                level = ?, level_title = ?, xp_percent = ?, plant_stage = ?, last_active_date = ?
            WHERE id = 1
        ''', (new_xp, new_bottles, new_co2, new_water, level, title, xp_pct, plant_stage, datetime.date.today().isoformat()))

        if new_water >= 8:
            c.execute('UPDATE badges SET unlocked = 1, unlocked_at = ? WHERE badge_id = "hydration_hero" AND unlocked = 0', (datetime.date.today().isoformat(),))

        conn.commit()
    conn.close()
    return get_user_profile()

# =========================================================
# WORKOUT LOGGING & STREAK TRACKER
# =========================================================

def log_workout(workout_name, workout_type="Strength", duration="10 Mins", equipment="Bodyweight", intensity="Moderate", calories=60, xp=35):
    conn = get_db()
    c = conn.cursor()
    today_str = datetime.date.today().isoformat()
    now_human = datetime.datetime.now().strftime("%b %d at %I:%M %p")

    c.execute('''
        INSERT INTO workout_logs (workout_name, workout_type, duration, equipment, intensity, calories_est, xp_earned, date_str, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (workout_name, workout_type, duration, equipment, intensity, calories, xp, today_str, now_human))

    c.execute('UPDATE daily_quests SET completed = 1, current = 1 WHERE quest_id = "workout_session" AND date_str = ?', (today_str,))
    c.execute('UPDATE badges SET unlocked = 1, unlocked_at = ? WHERE badge_id = "workout_warrior" AND unlocked = 0', (today_str,))

    conn.commit()
    conn.close()

    update_user_profile(xp_add=xp)
    return get_workout_stats()

def get_workout_logs(limit=20):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM workout_logs ORDER BY id DESC LIMIT ?', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_workout_log(log_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM workout_logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()
    return get_workout_stats()

def get_workout_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT DISTINCT date_str FROM workout_logs ORDER BY date_str DESC')
    dates = [r[0] for r in c.fetchall()]

    c.execute('SELECT COUNT(*), SUM(calories_est), SUM(xp_earned) FROM workout_logs')
    totals = c.fetchone()
    total_workouts = totals[0] or 0
    total_calories = totals[1] or 0
    total_xp = totals[2] or 0

    conn.close()

    streak = 0
    if dates:
        today = datetime.date.today()
        current_check = today

        first_date = datetime.date.fromisoformat(dates[0])
        if first_date == today or first_date == (today - datetime.timedelta(days=1)):
            current_check = first_date
            date_set = set(dates)
            while current_check.isoformat() in date_set:
                streak += 1
                current_check = current_check - datetime.timedelta(days=1)

    return {
        'streak': max(1, streak) if total_workouts > 0 else 0,
        'total_workouts': total_workouts,
        'total_calories': total_calories,
        'total_xp': total_xp
    }

# =========================================================
# READING PROGRESS & BOOKMARKS
# =========================================================

def save_reading_progress(book_id, page_num):
    conn = get_db()
    c = conn.cursor()
    now_str = datetime.date.today().isoformat()
    c.execute('''
        INSERT INTO reading_progress (book_id, current_page, total_pages, last_read_at)
        VALUES (?, ?, 3, ?)
        ON CONFLICT(book_id) DO UPDATE SET current_page = excluded.current_page, last_read_at = excluded.last_read_at
    ''', (book_id, page_num, now_str))
    conn.commit()
    conn.close()
    update_user_profile(xp_add=10)

def get_reading_progress(book_id=None):
    conn = get_db()
    c = conn.cursor()
    if book_id:
        c.execute('SELECT * FROM reading_progress WHERE book_id = ?', (book_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else {'book_id': book_id, 'current_page': 1, 'total_pages': 3}
    else:
        c.execute('SELECT * FROM reading_progress')
        rows = {r['book_id']: dict(r) for r in c.fetchall()}
        conn.close()
        return rows

# =========================================================
# DOODLE STUDIO & SAVED ARTWORKS
# =========================================================

def save_doodle(author, title, image_data):
    conn = get_db()
    c = conn.cursor()
    now_str = datetime.datetime.now().strftime("%b %d at %I:%M %p")
    if not author or author.strip() == "":
        author = "Anonymous Artist"
    if not title or title.strip() == "":
        title = "Dorm Canvas Sketch"

    c.execute('''
        INSERT INTO doodles (author, title, image_data, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (author.strip(), title.strip(), image_data, now_str))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    update_user_profile(xp_add=25)
    return new_id

def get_doodles(limit=30):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, author, title, image_data, timestamp FROM doodles ORDER BY id DESC LIMIT ?', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_doodle_by_id(doodle_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM doodles WHERE id = ?', (doodle_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_doodle(doodle_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM doodles WHERE id = ?', (doodle_id,))
    conn.commit()
    conn.close()
    return True

# =========================================================
# DIAGNOSTICS & LITERARY CORNER
# =========================================================

def add_history_log(sleep, screen, stress, mood, transport, distance, diet, co2, burnout, burnout_class, xp_earned):
    conn = get_db()
    c = conn.cursor()
    now_str = datetime.datetime.now().strftime("%b %d at %I:%M %p")
    c.execute('''
        INSERT INTO history_logs (timestamp, sleep, screen, stress, mood, transport, distance, diet, co2, burnout, burnout_class, xp_earned)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (now_str, sleep, screen, stress, mood, transport, distance, diet, co2, burnout, burnout_class, xp_earned))

    c.execute('SELECT COUNT(*) FROM history_logs')
    count = c.fetchone()[0]
    if count >= 1:
        c.execute('UPDATE badges SET unlocked = 1, unlocked_at = ? WHERE badge_id = "first_diagnostic" AND unlocked = 0', (datetime.date.today().isoformat(),))
    if transport in ['Bike / Walking (Zero CO₂)', 'Bicycle / Walking (Zero CO₂)', 'Bike Walk']:
        c.execute('UPDATE badges SET unlocked = 1, unlocked_at = ? WHERE badge_id = "zero_emission" AND unlocked = 0', (datetime.date.today().isoformat(),))

    conn.commit()
    conn.close()

def get_history_logs(limit=25):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM history_logs ORDER BY id DESC LIMIT ?', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_literary_posts():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM literary_posts ORDER BY id DESC')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def add_literary_post(author, title, content, tag='Student Voice'):
    conn = get_db()
    c = conn.cursor()
    now_str = datetime.datetime.now().strftime("Today at %I:%M %p")
    if not author or author.strip() == "":
        author = "Anonymous Writer"

    c.execute('''
        INSERT INTO literary_posts (author, title, content, tag, likes, timestamp)
        VALUES (?, ?, ?, ?, 1, ?)
    ''', (author.strip(), title.strip(), content.strip(), tag, now_str))
    c.execute('UPDATE badges SET unlocked = 1, unlocked_at = ? WHERE badge_id = "literary_bard" AND unlocked = 0', (datetime.date.today().isoformat(),))
    conn.commit()
    conn.close()
    update_user_profile(xp_add=35)

def like_literary_post(post_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE literary_posts SET likes = likes + 1 WHERE id = ?', (post_id,))
    c.execute('SELECT likes FROM literary_posts WHERE id = ?', (post_id,))
    row = c.fetchone()
    new_likes = row[0] if row else 0
    conn.commit()
    conn.close()
    update_user_profile(xp_add=5)
    return new_likes

def get_daily_quests():
    ensure_daily_quests()
    today = datetime.date.today().isoformat()
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM daily_quests WHERE date_str = ? ORDER BY id ASC', (today,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def complete_daily_quest(quest_id):
    today = datetime.date.today().isoformat()
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT xp_reward, completed FROM daily_quests WHERE quest_id = ? AND date_str = ?', (quest_id, today))
    row = c.fetchone()
    awarded_xp = 0
    if row and row['completed'] == 0:
        awarded_xp = row['xp_reward']
        c.execute('UPDATE daily_quests SET completed = 1, current = target WHERE quest_id = ? AND date_str = ?', (quest_id, today))
        conn.commit()
        update_user_profile(xp_add=awarded_xp)
    conn.close()
    return awarded_xp

def log_focus_session(minutes):
    conn = get_db()
    c = conn.cursor()
    now_str = datetime.datetime.now().strftime("%b %d, %I:%M %p")
    c.execute('INSERT INTO focus_sessions (minutes, timestamp, completed) VALUES (?, ?, 1)', (minutes, now_str))
    if minutes >= 20:
        c.execute('UPDATE badges SET unlocked = 1, unlocked_at = ? WHERE badge_id = "deep_focus" AND unlocked = 0', (datetime.date.today().isoformat(),))
    conn.commit()
    conn.close()
    earned = minutes * 2
    update_user_profile(xp_add=earned)
    return earned

def get_badges():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM badges ORDER BY id ASC')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

init_db()
