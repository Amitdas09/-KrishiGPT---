import streamlit as st
import whisper
import requests
from gtts import gTTS
from langdetect import detect
import tempfile
import os
from datetime import datetime
import json
from audio_recorder_streamlit import audio_recorder

# Page configuration
st.set_page_config(
    page_title="KrishiGPT - किसान सहायक",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI - DARK THEME
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #81C784;
        text-align: center;
        margin-bottom: 2rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .advice-card {
        background: #1e1e1e !important;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .advice-card h3 {
        color: #4CAF50 !important;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .advice-card p {
        color: #ffffff !important;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    .stMarkdown {
        color: #ffffff !important;
    }
    .stExpander {
        background-color: #2d2d2d !important;
        border: 1px solid #4CAF50 !important;
    }
    .stExpander p, .stExpander div {
        color: #ffffff !important;
    }
    [data-testid="stExpander"] {
        background-color: #2d2d2d !important;
    }
    [data-testid="stExpander"] p {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #388E3C;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'whisper_model' not in st.session_state:
    st.session_state.whisper_model = None

# Initialize Whisper model (cached)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("medium")

# Get weather data
def get_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'city': data['name']
        }
        return weather_info
    except Exception as e:
        st.error(f"Weather data error: {str(e)}")
        return None

# Detect language
def detect_language(text):
    """Detect language of input text"""
    try:
        lang = detect(text)
        return 'hi' if lang == 'hi' else 'en'
    except:
        return 'en'

# Generate response using LLaMA via Ollama
def generate_response(query, weather_data, language):
    """Generate agricultural advice using LLaMA 3.2 3B via Ollama"""
    try:
        # Prepare context with weather information
        weather_context = ""
        if weather_data:
            weather_context = f"""
Current Weather in {weather_data['city']}:
- Temperature: {weather_data['temperature']}°C (Feels like: {weather_data['feels_like']}°C)
- Humidity: {weather_data['humidity']}%
- Conditions: {weather_data['description']}
- Wind Speed: {weather_data['wind_speed']} m/s
- Pressure: {weather_data['pressure']} hPa
"""
        
        # Create prompt based on language
        if language == 'hi':
            system_prompt = """तुम एक विशेषज्ञ कृषि सलाहकार हो जो भारतीय किसानों की मदद करता है। 
वर्तमान मौसम की स्थिति के आधार पर व्यावहारिक और विस्तृत सलाह दो।
केवल हिंदी में जवाब दो। सरल और समझने योग्य भाषा का उपयोग करो।"""
            user_prompt = f"{weather_context}\n\nकिसान का सवाल: {query}\n\nकृपया मौसम को ध्यान में रखते हुए विस्तृत सलाह दें।"
        else:
            system_prompt = """You are an expert agricultural advisor helping Indian farmers.
Provide practical and detailed advice based on current weather conditions.
Respond only in English. Use simple and understandable language."""
            user_prompt = f"{weather_context}\n\nFarmer's Question: {query}\n\nPlease provide detailed advice considering the weather."
        
        # Call Ollama API
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2:3b",
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        return result['response'].strip()
    
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        st.error(error_msg)
        return "क्षमा करें, मैं अभी जवाब नहीं दे सकता। कृपया फिर से प्रयास करें।" if language == 'hi' else "Sorry, I cannot respond right now. Please try again."

# Text to speech
def text_to_speech(text, language):
    """Convert text to speech using gTTS"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

# Main UI
def main():
    # Header
    st.markdown('<div class="main-header">🌾 KrishiGPT - किसान सहायक</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">आवाज से पूछें, हिंदी या अंग्रेजी में | Ask by Voice, in Hindi or English</div>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # OpenWeatherMap API Key (pre-filled)
        api_key = "def991daa63f5aa42c310f7bad13dbce"
        
        # Location input
        city = st.text_input(
            "Your City / आपका शहर",
            value="Delhi",
            help="Enter your city name for weather information"
        )
        
        # Language preference
        preferred_lang = st.selectbox(
            "Preferred Language / पसंदीदा भाषा",
            ["Auto-detect", "Hindi (हिंदी)", "English"],
            index=0
        )
        
        st.divider()
        
        # Info section
        st.markdown("<h2 style='color: #ffffff;'>ℹ️ How to Use</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div style='color: #ffffff;'>
        <ol>
            <li>Set your city name</li>
            <li>Click the microphone to record</li>
            <li>Ask your farming question</li>
            <li>Get weather-aware advice</li>
        </ol>
        <p><strong>Supported Languages:</strong></p>
        <ul>
            <li>Hindi (हिंदी)</li>
            <li>English</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Check Ollama status
        try:
            ollama_check = requests.get("http://localhost:11434/api/tags", timeout=5)
            if ollama_check.status_code == 200:
                st.success("✅ Ollama Connected")
            else:
                st.warning("⚠️ Ollama Not Responding")
        except:
            st.error("❌ Ollama Not Running")
            st.info("Start Ollama with: `ollama serve`")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Weather card
        if api_key and city:
            weather_data = get_weather_data(city, api_key)
            if weather_data:
                st.markdown(f"""
                <div class="weather-card">
                    <h3>🌤️ Current Weather - {weather_data['city']}</h3>
                    <p style="font-size: 2rem; margin: 0.5rem 0;">
                        {weather_data['temperature']}°C
                    </p>
                    <p>{weather_data['description'].title()}</p>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <p>💧 Humidity: {weather_data['humidity']}%</p>
                    <p>💨 Wind: {weather_data['wind_speed']} m/s</p>
                    <p>🌡️ Feels like: {weather_data['feels_like']}°C</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Enter city name to see weather")
    
    with col1:
        # Input methods
        st.subheader("Ask Your Question / अपना सवाल पूछें")
        
        input_method = st.radio(
            "Input Method",
            ["🎤 Voice Input", "⌨️ Text Input"],
            horizontal=True
        )
        
        query = ""
        
        if input_method == "🎤 Voice Input":
            st.info("Click the button below to start recording")
            
            # Audio recorder
            audio_bytes = audio_recorder(
                text="Click to Record",
                recording_color="#e74c3c",
                neutral_color="#2E7D32",
                icon_name="microphone",
                icon_size="3x"
            )
            
            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")
                
                # Save audio temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                    temp_audio.write(audio_bytes)
                    temp_audio_path = temp_audio.name
                
                # Transcribe using Whisper
                with st.spinner("Transcribing... / लिख रहे हैं..."):
                    try:
                        if st.session_state.whisper_model is None:
                            st.session_state.whisper_model = load_whisper_model()
                        
                        result = st.session_state.whisper_model.transcribe(temp_audio_path)
                        query = result["text"]
                        st.success(f"**Transcribed / लिखा गया:** {query}")
                    except Exception as e:
                        st.error(f"Transcription error: {str(e)}")
                    finally:
                        os.unlink(temp_audio_path)
        
        else:
            query = st.text_area(
                "Type your question here",
                height=100,
                placeholder="E.g., What crops should I plant in this weather? / इस मौसम में कौन सी फसल लगाऊं?"
            )
        
        # Generate response button
        if st.button("🌾 Get Advice / सलाह पाएं", use_container_width=True):
            if not query:
                st.warning("Please provide a question / कृपया एक सवाल पूछें")
            else:
                # Detect language
                detected_lang = detect_language(query)
                
                if preferred_lang == "Hindi (हिंदी)":
                    detected_lang = 'hi'
                elif preferred_lang == "English":
                    detected_lang = 'en'
                
                lang_name = "Hindi" if detected_lang == 'hi' else "English"
                st.info(f"Detected Language: {lang_name}")
                
                # Get weather data
                weather_data = get_weather_data(city, api_key) if city else None
                
                # Generate response
                with st.spinner("Generating advice... / सलाह तैयार कर रहे हैं..."):
                    response = generate_response(query, weather_data, detected_lang)
                
                # Display response with better visibility
                st.markdown(f"""
                <div class="advice-card">
                    <h3>💡 Agricultural Advice / कृषि सलाह</h3>
                    <p>{response}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate audio response
                with st.spinner("Generating audio... / आवाज बना रहे हैं..."):
                    audio_file = text_to_speech(response, detected_lang)
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        os.unlink(audio_file)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'query': query,
                    'response': response,
                    'language': lang_name
                })
    
    # Chat History
    if st.session_state.chat_history:
        st.divider()
        st.subheader("📜 Chat History / बातचीत का इतिहास")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"Q: {chat['query'][:50]}... ({chat['timestamp']})"):
                st.markdown(f"<p style='color: #ffffff; font-weight: bold;'>Language: {chat['language']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #ffffff;'><strong>Question:</strong> {chat['query']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #ffffff;'><strong>Answer:</strong> {chat['response']}</p>", unsafe_allow_html=True)
        
        if st.button("Clear History / इतिहास साफ़ करें"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()