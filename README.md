# 🧠 Mental Health Companion Chatbot

A supportive, AI-powered chatbot designed to help students manage stress, anxiety, and loneliness through sentiment analysis, empathetic responses, and personalized relaxation techniques.

## Features

✨ **Key Capabilities:**
- **Mood Detection**: Analyzes user sentiment using TextBlob to detect emotional state
- **Empathetic Responses**: Uses Groq AI (Mixtral 8x7B) to generate compassionate, supportive messages
- **Relaxation Tips**: Provides mood-specific relaxation and coping strategies
- **Conversation History**: Maintains chat history and mood tracking
- **Crisis Resources**: Quick access to mental health hotlines and support services
- **Beautiful UI**: Clean, welcoming interface built with Streamlit

## Installation

### 1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Get Groq API Key**

1. Visit [Groq Console](https://console.groq.com)
2. Sign up for a free account
3. Create an API key in the dashboard
4. Copy your API key

### 3. **Set Up Environment Variables**

1. Rename `.env.example` to `.env`:
```bash
mv .env.example .env
```

2. Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_actual_api_key_here
```

## Running the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

1. **User Input**: Type your feelings or thoughts into the chat box
2. **Mood Detection**: The app analyzes your message sentiment (positive, neutral, negative)
3. **AI Response**: Groq generates an empathetic, supportive response
4. **Relaxation Tips**: Receive personalized wellness suggestions based on your mood
5. **Track Progress**: View your mood history in the dashboard

## Technology Stack

- **Streamlit**: Interactive web interface
- **TextBlob**: Sentiment analysis for mood detection
- **Groq**: Fast LLM API (Mixtral 8x7B model)
- **Python-dotenv**: Secure environment variable management

## Key Components

### Sentiment Analysis
- Polarity scoring: -1 (very negative) to +1 (very positive)
- Classification: Positive (>0.1), Neutral (-0.1 to 0.1), Negative (<-0.1)

### Response Generation
- System prompt ensures empathetic, supportive tone
- Temperature: 0.7 (balanced creativity and consistency)
- Max tokens: 300 (concise but thorough responses)

### Relaxation Tips Database
- 10 negative mood tips (deep breathing, walking, music, journaling, etc.)
- 6 neutral mood tips (goal-setting, learning, exercise, etc.)
- 6 positive mood tips (celebration, gratitude, kindness, etc.)

## Resources & Support

If you or someone you know is struggling:

- **Crisis Text Line**: Text HOME to 741741
- **National Suicide Prevention Lifeline (US)**: 988
- **International**: Visit [findahelpline.com](https://findahelpline.com)

## Important Disclaimer

⚠️ **This chatbot is a support tool, not a replacement for professional mental health care.**

If you're experiencing:
- Suicidal thoughts
- Severe depression or anxiety
- Self-harm urges
- Crisis situations

**Please reach out to a mental health professional or emergency service immediately.**

## Future Enhancements

- [ ] User accounts and persistent data
- [ ] Mood tracking visualizations
- [ ] Recommended professional resources by location
- [ ] Integration with calendar for stress management
- [ ] Voice input/output support
- [ ] Multi-language support
- [ ] Customizable relaxation exercises (videos, guided meditation)

## License

This project is open-source and available for educational purposes.

---

**Remember**: You're not alone. Taking care of your mental health is an act of self-love. 💙
