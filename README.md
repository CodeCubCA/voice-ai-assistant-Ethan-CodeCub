# 🤖 AI Voice Chat Assistant

A powerful AI chatbot web application built with Streamlit and Google Gemini API, featuring advanced voice input capabilities, multi-language support, and customizable AI personalities.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎤 Advanced Voice Input
- **Voice Recording**: Click-to-record microphone interface
- **Speech-to-Text**: Automatic transcription using Google Speech Recognition
- **Multi-Language Support**: 12 languages including English, French, Spanish, German, Chinese, Japanese, Korean, Italian, Portuguese, Russian, Arabic, and Hindi
- **Ambient Noise Adjustment**: Automatic noise reduction for better accuracy
- **Visual Feedback**: Real-time status updates and transcription display

### 🎭 Multiple AI Personalities
Choose from different AI personalities to match your needs:
- **Can Do Everything AI Buddy** - Versatile assistant for any task
- **Chat Everything** - Friendly conversationalist for casual chats
- **Game Professional** - Expert gaming advisor and strategist
- **Study Buddy** - Patient tutor for learning any subject

### 🗣️ Voice Commands
Control the app with your voice:
- `"Clear chat"` - Clear conversation history
- `"Change personality to [name]"` - Switch AI personalities
- `"What can you do?"` - Show available commands and help

### 💬 Chat Features
- **Conversation History**: Maintains context throughout the session
- **Dual Input Methods**: Type or speak your messages
- **Real-time Responses**: Powered by Google Gemini 2.5 Flash
- **Beautiful UI**: Clean, modern interface with chat bubbles

## 🚀 Getting Started

### Prerequisites
- Python 3.13 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voice-ai-chatbot.git
   cd voice-ai-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8502`
   - Or manually navigate to the URL shown in the terminal

## 📋 Usage

### Text Input
1. Type your message in the chat input box at the bottom
2. Press Enter to send
3. AI responds instantly with context-aware answers

### Voice Input
1. Click the microphone button
2. Speak your message clearly
3. Click stop when finished
4. The app transcribes and sends automatically

### Changing Language
1. Open the sidebar
2. Find "Language Settings"
3. Select your preferred language from the dropdown
4. Voice input will now recognize that language

### Using Voice Commands
Simply speak these commands:
- "Clear chat" - Resets conversation
- "Change personality to Study Buddy" - Switches AI personality
- "What can you do?" - Shows help information

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Speech Recognition**: Google Speech Recognition API
- **Audio Recording**: audio-recorder-streamlit
- **Language**: Python 3.13

## 📦 Dependencies

```
streamlit>=1.31.0
google-generativeai>=0.3.2
python-dotenv>=1.0.0
audio-recorder-streamlit>=0.0.8
SpeechRecognition>=3.10.0
pydub>=0.25.1
```

## 🌍 Supported Languages

| Language | Code |
|----------|------|
| English | en-US |
| French | fr-FR |
| Spanish | es-ES |
| German | de-DE |
| Chinese (Mandarin) | zh-CN |
| Japanese | ja-JP |
| Korean | ko-KR |
| Italian | it-IT |
| Portuguese | pt-BR |
| Russian | ru-RU |
| Arabic | ar-SA |
| Hindi | hi-IN |

## 🎯 Key Features Explained

### Personality System
Each personality has a unique system prompt that shapes how the AI responds:
- **AI Buddy**: Helpful and enthusiastic, tackles any challenge
- **Chat Buddy**: Engaging conversationalist, great listener
- **Gaming Pro**: Expert in gaming strategies and industry knowledge
- **Study Buddy**: Patient educator, adapts to learning styles

### Voice Activity Detection
- Real-time status indicators show recording state
- Visual feedback during transcription
- Success/error messages with helpful tips

### Smart Command Processing
- Natural language understanding for commands
- Case-insensitive matching
- Instant execution with visual confirmation

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Customizing Personalities
Edit the `PERSONALITIES` dictionary in `app.py`:
```python
PERSONALITIES = {
    "Your Custom Personality": {
        "name": "Custom Name",
        "icon": "🎨",
        "system_prompt": "Your custom system prompt here...",
        "description": "Brief description"
    }
}
```

## 🐛 Troubleshooting

### Voice Input Not Working
- Ensure microphone permissions are granted
- Check that the correct language is selected
- Speak clearly in a quiet environment
- Verify internet connection for speech recognition

### API Errors
- Verify your Gemini API key is correct in `.env`
- Check API quota and usage limits
- Ensure stable internet connection

### Installation Issues
- Update pip: `pip install --upgrade pip`
- Use Python 3.13+: `python --version`
- Try creating a virtual environment

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for the AI model
- [Streamlit](https://streamlit.io/) for the web framework
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) for voice input
- [audio-recorder-streamlit](https://github.com/Jooui/audio-recorder-streamlit) for the microphone component

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit and Google Gemini API**
