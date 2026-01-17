import streamlit as st
from textblob import TextBlob
import random
from datetime import datetime, timedelta
from groq import Groq
import os
from dotenv import load_dotenv
st.set_page_config(
    page_title="Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Load environment variables
load_dotenv()

# Initialize session state EARLY (THIS PART)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

if "client" not in st.session_state:
    st.session_state.client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

with st.sidebar:

    st.header("📋 Your Wellness Dashboard")

    # ---------- Mood Counters ----------
    if st.session_state.mood_history:
        mood_counts = {
            "😊": st.session_state.mood_history.count("😊"),
            "😐": st.session_state.mood_history.count("😐"),
            "😔": st.session_state.mood_history.count("😔")
        }

        col1, col2, col3 = st.columns(3)
        col1.metric("Positive", mood_counts["😊"])
        col2.metric("Neutral", mood_counts["😐"])
        col3.metric("Negative", mood_counts["😔"])
    else:
        st.caption("No mood data yet 🌱")

    st.divider()

    # ---------- Mood Overview ----------
    st.subheader("📊 Mood Overview")

    if st.session_state.mood_history:
        chart_data = {
            "Positive": mood_counts["😊"],
            "Neutral": mood_counts["😐"],
            "Negative": mood_counts["😔"]
        }
        st.bar_chart(chart_data)
    else:
        st.caption("Track your mood to see insights")

    st.divider()

    # ---------- Calm Me Now ----------
    st.subheader("🚨 Calm Me Now")

    if st.button("🫶 I need calm"):
        st.info("You’re safe. Let’s slow things down together 💙")
        st.write("🫁 **Breathe with me:**")
        st.write("• Inhale for 4 seconds")
        st.write("• Hold for 4 seconds")
        st.write("• Exhale for 6 seconds")
        st.write("Repeat this 5 times 🌿")

    st.divider()

    # ---------- Guided Breathing ----------
    st.subheader("🫁 Guided Breathing")

    breath = st.selectbox(
        "Choose a breathing rhythm",
        ["4-4-4 (Box)", "4-7-8 (Relax)", "5-5 (Slow)"]
    )

    if st.button("▶ Start Breathing"):
        if breath == "4-4-4 (Box)":
            st.success("Inhale 4 • Hold 4 • Exhale 4")
        elif breath == "4-7-8 (Relax)":
            st.success("Inhale 4 • Hold 7 • Exhale 8")
        else:
            st.success("Inhale 5 • Exhale 5")

    st.divider()

    # ---------- Resources ----------
    st.subheader("🆘 Resources & Support")
    st.info(
        "**If you're in crisis:**\n"
        "- Crisis Text Line: Text HOME to 741741\n"
        "- Suicide Prevention Lifeline: 988\n"
        "- International: findahelpline.com"
    )

    st.divider()

    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.mood_history = []
        st.success("Conversation cleared!")

if "last_checkin_date" not in st.session_state:
    st.session_state.last_checkin_date = None

if "current_streak" not in st.session_state:
    st.session_state.current_streak = 0

if "longest_streak" not in st.session_state:
    st.session_state.longest_streak = 0


# Custom CSS
theme = st.session_state.theme

# Theme CSS
st.markdown("""
<style>
:root {
    --bg-color: radial-gradient(circle at top, #0f172a, #020617);
    --card-bg: linear-gradient(145deg, #121826, #0e1320);
    --sidebar-card-bg: linear-gradient(180deg, #111827, #020617);

    --text-color: #e5e7eb;
    --subtext-color: #9ca3af;

    --accent: #60a5fa;
    --accent-2: #34d399;
    --warning: #fbbf24;
    --danger: #f87171;
    --purple: #a78bfa;

    --border-color: rgba(255,255,255,0.08);
}
.emotion-badge.positive {
    background: linear-gradient(135deg, #34d399, #059669);
}

.emotion-badge.neutral {
    background: linear-gradient(135deg, #fbbf24, #d97706);
}

.emotion-badge.negative {
    background: linear-gradient(135deg, #f87171, #dc2626);
}

section[data-testid="stMain"] > div {
    animation: fadeUp 0.5s ease both;
}

/* App background */
.stApp {
    background: var(--bg-color);
}

/* Cards */
.stInfo, .stSuccess, .stWarning {
    background: var(--card-bg) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border);
    transition: transform .3s ease, box-shadow .3s ease;
}

.stInfo:hover {
    box-shadow: 0 0 20px rgba(96,165,250,.35);
    transform: translateY(-4px);
}

.stSuccess:hover {
    box-shadow: 0 0 20px rgba(52,211,153,.35);
}

.stWarning:hover {
    box-shadow: 0 0 20px rgba(248,113,113,.35);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--blue), var(--purple)) !important;
    color: white !important;
    border-radius: 12px;
    border: none;
    transition: transform .25s ease, box-shadow .25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 12px 30px rgba(96,165,250,.45);
}

/* Chat animation */
.stChatMessage {
    background: var(--card-bg) !important;
    border-radius: 14px;
    animation: chatPop .35s ease-out;
}

@keyframes chatPop {
    from { opacity: 0; transform: translateY(12px) scale(.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

/* Emotion badge */
.emotion-badge {
    padding: 6px 16px;
    border-radius: 999px;
    animation: pulse 2.5s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 rgba(96,165,250,0); }
    50% { box-shadow: 0 0 16px rgba(96,165,250,.45); }
    100% { box-shadow: 0 0 0 rgba(96,165,250,0); }
}
</style>
""", unsafe_allow_html=True)

# Common + Animation CSS
st.markdown("""
<style>
/* ================== WORKSPACE (MAIN AREA) ================== */
/* MAIN WORKSPACE – theme aware */
/* Fix inner text elements inside main area */

/* MAIN CONTENT TEXT – SAFE FIX */
section[data-testid="stMain"] {
    color: var(--text-color);
}

.stApp {
    background-color: var(--bg-color);
}


/* ================== SIDEBAR ================== */
/* Sidebar container background */
section[data-testid="stSidebar"] {
    background-color: var(--sidebar-card-bg) !important;
}


/* Sidebar main text */
.stSidebar h1,
.stSidebar h2,
.stSidebar h3,
.stSidebar h4,
.stSidebar h5,
.stSidebar h6,
.stSidebar p,
.stSidebar label {
    color: var(--text-color) !important;
}

/* Sidebar secondary text */
.stSidebar small,
.stSidebar .stMarkdown em,
.stSidebar .stMetricLabel {
    color: #d1d5db !important;
}

/* Sidebar metric values */
.stSidebar .stMetricValue {
    color: var(--text-color) !important;
}


/* Page animation */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}


/* Chat animation */
@keyframes bubbleIn {
    0% { opacity: 0; transform: translateY(12px) scale(0.96); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

.stChatMessage {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color);
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    animation: bubbleIn 0.35s ease-out;
    border-radius: 14px;
}

/* Emotion glow */
@keyframes glow {
    0% { box-shadow: 0 0 0 rgba(79,70,229,0); }
    50% { box-shadow: 0 0 12px rgba(79,70,229,0.35); }
    100% { box-shadow: 0 0 0 rgba(79,70,229,0); }
}

.emotion-badge {
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    animation: glow 2.5s infinite;
}

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: white;
    border-radius: 10px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 12px 25px rgba(0,0,0,0.18);
}

/* Sidebar text (ONLY what we need) */
.stSidebar h1,
.stSidebar h2,
.stSidebar h3,
.stSidebar h4,
.stSidebar h5,
.stSidebar h6,
.stSidebar p,
.stSidebar span,
.stSidebar label,
.stSidebar li {
    color: var(--text-color) !important;
}

/* Sidebar secondary text */
.stSidebar small,
.stSidebar .stMarkdown em,
.stSidebar .stMetricLabel {
    color: #d1d5db !important;
}

/* Sidebar metric numbers */
.stSidebar .stMetricValue {
    color: #ffffff !important;
}


/* Muted sidebar secondary text */
.stSidebar small,
.stSidebar .stMarkdown em {
    color: #d1d5db !important;
}

/* Sidebar cards */
.stSidebar .stMarkdown,
.stSidebar .stInfo,
.stSidebar .stMetric,
.stSidebar .stButton {
    background: var(--sidebar-card-bg);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* Sidebar section headers */
.stSidebar h3 {
    font-weight: 600;
    letter-spacing: 0.2px;
    color: var(--text-color) !important;
}


/* Sidebar buttons */
.stSidebar .stButton > button {
    width: 100%;
}
/* Sidebar dividers */
.stSidebar hr {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 16px 0;
}

/* Smooth theme switch */
* {
    transition: background-color 0.3s ease, color 0.3s ease;
}
/* Page fade-in animation */
@keyframes pageFade {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stApp {
    animation: pageFade 0.6s ease-out;
}
/* Title animation */
@keyframes titleSlide {
    from {
        opacity: 0;
        transform: translateY(-12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

section[data-testid="stMain"] h1 {
    animation: titleSlide 0.7s ease-out;
}
/* Chat bubble animation */
@keyframes chatBubble {
    0% {
        opacity: 0;
        transform: translateY(8px) scale(0.97);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.stChatMessage {
    animation: chatBubble 0.35s ease-out;
}
/* Button hover animation */
.stButton > button {
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}
/* Emotion glow */
@keyframes emotionGlow {
    0% { box-shadow: 0 0 0 rgba(96,165,250,0); }
    50% { box-shadow: 0 0 14px rgba(96,165,250,0.45); }
    100% { box-shadow: 0 0 0 rgba(96,165,250,0); }
}

.emotion-badge {
    animation: emotionGlow 2.5s infinite;
}


</style>
""", unsafe_allow_html=True)


# Relaxation tips database
RELAXATION_TIPS = {
    "negative": [
        "🧘 **Deep Breathing**: Breathe in for 4 counts, hold for 4, exhale for 4. Repeat 5 times.",
        "🚶 **Take a Walk**: A short walk in fresh air can help clear your mind and reduce stress.",
        "🎵 **Listen to Music**: Play your favorite calming or uplifting music.",
        "✍️ **Journaling**: Write down your thoughts and feelings to process them.",
        "🌞 **Get Sunlight**: Spend 10-15 minutes in natural sunlight.",
        "🤗 **Reach Out**: Talk to a friend or family member about how you're feeling.",
        "📱 **Digital Detox**: Take a break from screens for 15-30 minutes.",
        "💧 **Stay Hydrated**: Drink water and notice how you feel.",
        "🎨 **Creative Activity**: Draw, paint, or engage in a hobby you enjoy.",
        "🧘‍♀️ **Progressive Muscle Relaxation**: Tense and relax each muscle group."
    ],
    "neutral": [
        "💡 **Set a Goal**: What's one small thing you'd like to accomplish today?",
        "📚 **Learn Something**: Read an article or watch a video on a topic of interest.",
        "🤝 **Connect**: Reach out to someone you care about.",
        "🎯 **Plan Ahead**: Organize your week to feel more in control.",
        "💪 **Exercise**: A quick workout can boost your mood and energy.",
        "🧩 **Puzzle or Game**: Engage your mind with a fun challenge."
    ],
    "positive": [
        "🎉 **Celebrate**: Take time to acknowledge and celebrate your win!",
        "🤲 **Share Joy**: Tell someone about your good mood or achievement.",
        "📸 **Capture the Moment**: Take a photo to remember this positive feeling.",
        "🎁 **Do Something Kind**: Help someone else and spread the positivity.",
        "💭 **Gratitude**: List 3 things you're grateful for right now.",
        "🌟 **Momentum**: Use this positive energy to tackle something meaningful."
    ]
}

# Mood detection
def detect_mood(text):
    """Analyze sentiment and return mood category and polarity"""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        mood = "positive"
        emoji = "😊"
    elif polarity < -0.1:
        mood = "negative"
        emoji = "😔"
    else:
        mood = "neutral"
        emoji = "😐"
    
    return mood, emoji, polarity
# --------- MOOD-BASED SYSTEM PROMPTS ---------
MOOD_PROMPTS = {
    "positive": """
You are a warm, encouraging mental health companion.
Celebrate progress, reinforce positive emotions, and gently motivate.
Keep responses supportive and optimistic in 2–3 sentences.
""",

    "neutral": """
You are a calm, thoughtful mental health companion.
Help the user reflect, ask gentle questions, and offer balance.
Keep responses grounding and open-ended in 2–3 sentences.
""",

    "negative": """
You are a deeply empathetic mental health companion.
Validate emotions, provide reassurance, and reduce distress.
Use a calm, non-judgmental tone. Encourage support if needed.
Keep responses short and soothing in 2–3 sentences.
"""
}

# Get empathetic response from Groq
def get_empathetic_response(user_message, mood):
    system_prompt = MOOD_PROMPTS.get(
        mood,
        "You are a supportive mental health companion."
    )

    try:
        completion = st.session_state.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7 if mood != "negative" else 0.5,
            max_tokens=300
        )
        return completion.choices[0].message.content

    except Exception:
        return "I'm here with you. Would you like to tell me more?"

st.title("🧠 Mental Health Companion")
st.subheader("A safe space to talk about your feelings and get support")
st.caption("✨ You’re not alone. I’m here to listen.")
st.markdown("### 👋 Welcome")

st.markdown("How are you feeling right now?")

col1, col2, col3 = st.columns(3)

# 😊 GOOD
with col1:
    if st.button("😊 Good"):
        today = datetime.now().date()

        if st.session_state.last_checkin_date == today:
            pass
        elif st.session_state.last_checkin_date == today - timedelta(days=1):
            st.session_state.current_streak += 1
        else:
            st.session_state.current_streak = 1

        st.session_state.longest_streak = max(
            st.session_state.longest_streak,
            st.session_state.current_streak
        )

        st.session_state.last_checkin_date = today
        st.session_state.mood_history.append("😊")

        st.success("Glad to hear that! 💛")

# 😐 NEUTRAL
with col2:
    if st.button("😐 Neutral"):
        today = datetime.now().date()

        if st.session_state.last_checkin_date == today:
            pass
        elif st.session_state.last_checkin_date == today - timedelta(days=1):
            st.session_state.current_streak += 1
        else:
            st.session_state.current_streak = 1

        st.session_state.longest_streak = max(
            st.session_state.longest_streak,
            st.session_state.current_streak
        )

        st.session_state.last_checkin_date = today
        st.session_state.mood_history.append("😐")

        st.info("Thanks for checking in 🌱")

# 😔 NOT GREAT
with col3:
    if st.button("😔 Not great"):
        today = datetime.now().date()

        if st.session_state.last_checkin_date == today:
            pass
        elif st.session_state.last_checkin_date == today - timedelta(days=1):
            st.session_state.current_streak += 1
        else:
            st.session_state.current_streak = 1

        st.session_state.longest_streak = max(
            st.session_state.longest_streak,
            st.session_state.current_streak
        )

        st.session_state.last_checkin_date = today
        st.session_state.mood_history.append("😔")

        st.warning("I'm here for you 💙")
st.markdown("### 🔥 Mood Streak")

if st.session_state.current_streak > 0:
    st.success(
        f"🔥 Current streak: {st.session_state.current_streak} days\n\n"
        f"🏆 Longest streak: {st.session_state.longest_streak} days"
    )
else:
    st.info("Check in today to start your streak 🌱")

st.divider()
AFFIRMATIONS = [
    "You are doing the best you can, and that is enough.",
    "It’s okay to take things one step at a time.",
    "Your feelings are valid.",
    "You don’t have to have everything figured out today.",
    "Small progress is still progress."
]

daily_affirmation = random.choice(AFFIRMATIONS)

st.markdown("### 🌱 Daily Affirmation")
st.info(daily_affirmation)

st.divider()
WELLNESS_TIPS = [
    "Take 3 deep breaths and relax your shoulders.",
    "Drink a glass of water and notice how you feel.",
    "Stand up and stretch for 30 seconds.",
    "Take a short break from your screen.",
    "Write down one thing you’re grateful for."
]

st.markdown("### 💡 Wellness Tip")

if st.button("🔄 New Tip"):
    st.rerun()

st.info(random.choice(WELLNESS_TIPS))

st.divider()

st.markdown("""
<style>
.hero-line {
    margin-top: 6px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)
if not st.session_state.messages:
    st.markdown("💬 Start by sharing what’s on your mind. I’m here to listen.")


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])
        if "mood" in message:
            st.markdown(f"<span class='emotion-badge {message['mood']}'>{message['emoji']} {message['mood'].capitalize()}</span>", 
                       unsafe_allow_html=True)

# User input
user_input = st.chat_input("Share what's on your mind... 💭", key="user_input")

if user_input:
    # Detect mood
    mood, emoji, polarity = detect_mood(user_input)
    
    # Store mood history
    st.session_state.mood_history.append(emoji)
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "avatar": "👤",
        "mood": mood,
        "emoji": emoji
    })
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
        st.markdown(f"<span class='emotion-badge {mood}'>{emoji} {mood.capitalize()}</span>", 
                   unsafe_allow_html=True)
    
    # Get response from Groq
    with st.spinner("🤔 Thinking..."):
        response = get_empathetic_response(user_input, mood)
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "avatar": "🤖"
    })
    
    # Display response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
    
    # Provide relevant relaxation tips
    with st.container():
        st.divider()
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("💡 Try This")
        with col2:
            if st.button("🔄 Get Another Tip"):
                st.rerun()
        
        tip = random.choice(RELAXATION_TIPS[mood])
        st.info(tip)

# Footer
st.divider()
st.caption("🌟 Remember: This chatbot is here for support and guidance, but it's not a replacement for professional mental health care.")
st.caption("If you're struggling, please reach out to a mental health professional. You're not alone! 💙")

