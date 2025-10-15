# 🌾 KrishiGPT - किसान सहायक

**KrishiGPT** is a **multilingual AI-powered farming assistant** that helps Indian farmers get **personalized agricultural advice** using **voice or text** — in **Hindi** or **English**.  
It combines **OpenAI’s Whisper**, **Ollama’s LLaMA 3.2 model**, **Google Text-to-Speech**, and **OpenWeatherMap API** to provide **context-aware, weather-informed suggestions** for better crop management and decision-making.

---

## 🚀 Features

- 🗣️ **Voice or Text Input** — Ask your farming questions by speaking or typing   
- 🌦️ **Weather-Based Advice** — Integrates live weather data for context-specific suggestions  
- 🌐 **Multilingual Support** — Auto-detects and replies in Hindi 🇮🇳 or English 🇬🇧  
- 🧠 **AI-Powered Responses** — Uses **LLaMA 3.2 (3B)** model via **Ollama** for intelligent, context-rich answers  
- 🔊 **Text-to-Speech Output** — Generates spoken responses in your preferred language  
- 💬 **Chat History** — View your past questions and AI responses  
- 🌙 **Dark Theme UI** — Clean and modern interface for better visibility  

---

## 🏗️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **Speech Recognition** | [OpenAI Whisper](https://github.com/openai/whisper) |
| **Language Detection** | [langdetect](https://pypi.org/project/langdetect/) |
| **Text-to-Speech** | [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/) |
| **Weather Data** | [OpenWeatherMap API](https://openweathermap.org/api) |
| **AI Response Engine** | [Ollama + LLaMA 3.2](https://ollama.com/library/llama3.2) |
| **Audio Recorder** | [audio-recorder-streamlit](https://pypi.org/project/audio-recorder-streamlit/) |

---

## VISUAL DEMO
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/759772b6-dc23-4c1d-84fd-1def496a3ee9" />


## ⚙️ Installation

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/your-username/KrishiGPT.git
cd KrishiGPT
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Ollama
Install [Ollama](https://ollama.com/download) and pull the **LLaMA 3.2 (3B)** model:
```bash
ollama pull llama3.2:3b
ollama serve
```

### 5️⃣ Run the App
```bash
streamlit run app.py
```

---

## 🔑 API Keys

This project uses **OpenWeatherMap** for real-time weather updates.

- Get your free API key at: [https://openweathermap.org/api](https://openweathermap.org/api)
- Replace the default key in `app.py` with your own:
  ```python
  api_key = "YOUR_API_KEY"
  ```

---

## 🧩 Usage

1. Launch the app using Streamlit.  
2. Enter your **city name** in the sidebar.  
3. Choose **language** (Auto, Hindi, or English).  
4. Ask your question — either by typing or recording your voice.  
5. Get detailed, weather-aware **farming advice** with both **text and audio response**.  

---

## 📸 UI Preview

```
🌾 KrishiGPT - किसान सहायक
----------------------------------------
Ask by Voice or Text in Hindi or English
----------------------------------------
[🎤 Record Voice]   [⌨️ Type Text]

💡 Agricultural Advice / कृषि सलाह
----------------------------------------
🌤️ Current Weather - Delhi
Temperature: 32°C
Humidity: 68%
Advice: "In this weather, avoid overwatering wheat crops..."
----------------------------------------
```

---

## 🧠 Example Questions

- “इस मौसम में टमाटर की सिंचाई कितनी बार करनी चाहिए?”
- “Which fertilizer is best for paddy in high humidity?”
- “How to prevent pest infection in cotton crops?”

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use and modify with credit.

---

## 💚 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Ollama](https://ollama.com)
- [Google TTS](https://pypi.org/project/gTTS/)
- [OpenWeatherMap](https://openweathermap.org/api)
