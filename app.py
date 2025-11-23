import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
from gtts import gTTS
import tempfile
import base64

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Personality configurations
PERSONALITIES = {
    "AI Buddy": {
        "name": "AI Buddy",
        "icon": "🤖",
        "system_prompt": "You are a helpful, friendly, and enthusiastic AI assistant who can help with anything. You're capable, confident, and always ready to tackle any challenge. You approach every task with a positive attitude and provide clear, practical solutions.",
        "description": "A versatile AI assistant ready to help with any task"
    },
    "Chat Buddy": {
        "name": "Chat Buddy",
        "icon": "💬",
        "system_prompt": "You are a friendly conversationalist who loves to chat about absolutely anything! You're engaging, curious, and enjoy deep conversations on any topic - from everyday life to philosophy, hobbies, current events, random thoughts, and everything in between. You're a great listener and always keep the conversation flowing naturally.",
        "description": "A friendly companion for casual conversations about anything"
    },
    "Gaming Pro": {
        "name": "Gaming Pro",
        "icon": "🎮",
        "system_prompt": "You are an expert gaming professional with deep knowledge of video games across all platforms and genres. You provide strategic advice, tips, tricks, game recommendations, build guides, walkthroughs, and gaming industry insights. You're passionate about gaming culture and help players improve their skills and enjoy their gaming experience to the fullest.",
        "description": "Expert gaming advisor for strategies, tips, and game recommendations"
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "icon": "📚",
        "system_prompt": "You are a patient and supportive study companion who helps students learn effectively. You break down complex topics into understandable pieces, provide clear explanations, create study strategies, help with homework, offer practice questions, and motivate students to achieve their academic goals. You adapt your teaching style to each student's needs and make learning engaging and fun.",
        "description": "Your personal tutor for studying and learning any subject"
    }
}

# Initialize Streamlit page config
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chat Assistant")
    st.markdown("---")

    # Voice recorder at top
    st.subheader("🎤 Voice Recorder")
    st.write("Click the microphone to record")

    # Voice recorder in sidebar
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x"
    )

    st.markdown("---")

    # Personality selector
    st.subheader("Choose Personality")
    selected_personality = st.selectbox(
        "Select AI Personality:",
        options=list(PERSONALITIES.keys()),
        index=0
    )

    personality_config = PERSONALITIES[selected_personality]

    st.markdown("---")
    st.subheader("About")
    st.write(f"**{personality_config['icon']} {personality_config['name']}**")
    st.write(personality_config['description'])

    st.markdown("---")
    st.subheader("Information")
    st.write("**Model:** gemini-2.5-flash")
    st.write("**Powered by:** Google Gemini API")

    st.markdown("---")
    st.subheader("Language Settings")

    # Language selector
    LANGUAGES = {
        "English": "en-US",
        "French": "fr-FR",
        "Spanish": "es-ES",
        "German": "de-DE",
        "Chinese (Mandarin)": "zh-CN",
        "Japanese": "ja-JP",
        "Korean": "ko-KR",
        "Italian": "it-IT",
        "Portuguese": "pt-BR",
        "Russian": "ru-RU",
        "Arabic": "ar-SA",
        "Hindi": "hi-IN"
    }

    selected_language = st.selectbox(
        "Speech Recognition Language:",
        options=list(LANGUAGES.keys()),
        index=0,
        help="Select the language for voice input"
    )

    # Store language in session state
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"

    if selected_language != st.session_state.selected_language:
        st.session_state.selected_language = selected_language

    st.markdown("---")
    st.subheader("🔊 Audio Settings")

    # Auto-play TTS toggle
    auto_play_tts = st.toggle(
        "Auto-play AI responses",
        value=True,
        help="Automatically play audio for AI responses"
    )

    # Store in session state
    if "auto_play_tts" not in st.session_state:
        st.session_state.auto_play_tts = True

    if auto_play_tts != st.session_state.auto_play_tts:
        st.session_state.auto_play_tts = auto_play_tts

    st.markdown("---")
    st.subheader("Voice Input Tips")
    st.write("🎤 Click microphone to start")
    st.write("🗣️ Speak slowly and clearly")
    st.write("⏹️ Click stop when finished")
    st.write("✨ Best in quiet environments")

    st.markdown("---")
    st.subheader("Voice Commands")
    st.write("🔹 'Clear chat' - Clear history")
    st.write("🔹 'Change personality to [name]' - Switch AI")
    st.write("🔹 'What can you do?' - Show help")

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize current personality in session state
if "current_personality" not in st.session_state:
    st.session_state.current_personality = selected_personality

# Initialize voice input text in session state
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# Initialize TTS audio cache in session state
if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

# Initialize TTS processing flag
if "tts_processing" not in st.session_state:
    st.session_state.tts_processing = False

# Initialize last played message index
if "last_played_idx" not in st.session_state:
    st.session_state.last_played_idx = -1

# Reset chat if personality changed
if st.session_state.current_personality != selected_personality:
    st.session_state.messages = []
    st.session_state.current_personality = selected_personality

# Main chat interface
st.title(f"{personality_config['icon']} {selected_personality}")

# Create status placeholder for voice input feedback
status_placeholder = st.empty()

# Function to generate TTS audio
def generate_tts_audio(text, message_index):
    """Generate TTS audio for a message and cache it in session state"""
    # Check if audio already exists in cache
    if message_index in st.session_state.tts_audio:
        return st.session_state.tts_audio[message_index]

    try:
        # Create TTS object
        tts = gTTS(text=text, lang='en', slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)

            # Read the audio file as bytes
            with open(fp.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()

            # Clean up temporary file
            os.unlink(fp.name)

            # Cache the audio
            st.session_state.tts_audio[message_index] = audio_bytes

            return audio_bytes
    except Exception as e:
        # Silently fail for TTS errors to avoid disrupting the chat experience
        # User can still see the text response
        return None

# Function to process voice commands
def process_voice_command(text):
    """Process special voice commands and return True if a command was executed"""
    text_lower = text.lower().strip()

    # Clear chat command
    if "clear chat" in text_lower or "clear history" in text_lower or "delete chat" in text_lower:
        st.session_state.messages = []
        status_placeholder.success("✨ **Voice Command Executed:** Chat history cleared!")
        st.rerun()
        return True

    # Change personality command
    if "change personality" in text_lower or "switch personality" in text_lower or "switch to" in text_lower:
        for personality_name in PERSONALITIES.keys():
            if personality_name.lower() in text_lower:
                st.session_state.current_personality = personality_name
                st.session_state.messages = []
                status_placeholder.success(f"✨ **Voice Command Executed:** Switched to {personality_name}!")
                st.rerun()
                return True

        # If personality not found
        personalities_list = ", ".join(PERSONALITIES.keys())
        return f"I couldn't find that personality. Available options: {personalities_list}"

    # Help command
    if "what can you do" in text_lower or "help" in text_lower or "commands" in text_lower:
        help_text = """I can respond to these voice commands:
        - 'Clear chat' - Clears conversation history
        - 'Change personality to [name]' - Switches AI personality
        - I can also chat with you in multiple languages!"""
        return help_text

    return False

# Initialize prompt variable
prompt = None
command_response = None

# Get language code
LANGUAGES = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "German": "de-DE",
    "Chinese (Mandarin)": "zh-CN",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Italian": "it-IT",
    "Portuguese": "pt-BR",
    "Russian": "ru-RU",
    "Arabic": "ar-SA",
    "Hindi": "hi-IN"
}

# Process audio if recorded
if audio_bytes:
    # Check if this is a new recording
    if "last_audio" not in st.session_state or st.session_state.last_audio != audio_bytes:
        st.session_state.last_audio = audio_bytes

        # Show recording completed with visual effect
        status_placeholder.success("🎙️ **Recording completed!** Processing audio...")

        # Play back the audio
        with st.expander("🔊 Click to listen to your recording"):
            st.audio(audio_bytes, format="audio/wav")

        # Convert audio to text with language support
        with st.spinner("⏳ **Processing...** Converting speech to text..."):
            try:
                # Initialize recognizer
                recognizer = sr.Recognizer()

                # Convert bytes to audio file
                audio_data = sr.AudioFile(io.BytesIO(audio_bytes))

                with audio_data as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.record(source)

                # Get selected language code
                language_code = LANGUAGES.get(st.session_state.selected_language, "en-US")

                # Recognize speech using Google Speech Recognition with language support
                text = recognizer.recognize_google(audio, language=language_code)

                # Show success with transcription
                status_placeholder.success(f"✅ **Ready!** Transcribed: \"{text}\"")

                # Check for voice commands
                command_result = process_voice_command(text)

                if command_result == True:
                    # Command executed successfully (with rerun)
                    pass
                elif isinstance(command_result, str):
                    # Command returned a response
                    command_response = command_result
                    prompt = None
                else:
                    # No command detected, treat as regular message
                    prompt = text

            except sr.UnknownValueError:
                status_placeholder.error("❌ **Error:** Sorry, I couldn't understand the audio. Please try speaking more clearly and try again.")
            except sr.RequestError as e:
                status_placeholder.error(f"❌ **Error:** Could not connect to speech recognition service. Check your internet connection.")
            except Exception as e:
                status_placeholder.error(f"❌ **Error:** {str(e)}")
else:
    # Show ready status when no recording with animation
    status_placeholder.info("🎤 **Ready to record** - Click the microphone button to start")

st.markdown("---")

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Add TTS audio player for assistant messages (outside chat_message container)
    if message["role"] == "assistant" and st.session_state.auto_play_tts:
        # Generate audio for this message
        with st.spinner("🔊 Generating audio..."):
            audio_bytes = generate_tts_audio(message["content"], idx)

        if audio_bytes:
            # Show audio player for all assistant messages
            st.audio(audio_bytes, format='audio/mp3', autoplay=(idx == len(st.session_state.messages) - 1))
        else:
            st.warning("⚠️ Audio generation failed (rate limit or error)")

# Handle command responses
if command_response:
    with st.chat_message("assistant"):
        st.markdown(f"ℹ️ {command_response}")
    st.session_state.messages.append({"role": "assistant", "content": command_response})
    # The TTS will be handled in the next rerun when displaying messages

# Text input field - always show the typing box
user_input = st.chat_input("Type your message here or use voice input in sidebar...")

# Use voice prompt if available, otherwise use typed input
if not prompt and user_input:
    prompt = user_input

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Initialize the model
                model = genai.GenerativeModel('gemini-2.5-flash')

                # Prepare conversation history with system prompt
                chat_history = [
                    {"role": "user", "parts": [personality_config["system_prompt"]]},
                    {"role": "model", "parts": ["I understand. I'll respond according to this personality."]}
                ]

                # Add previous messages to history
                for msg in st.session_state.messages[:-1]:  # Exclude the last user message we just added
                    role = "user" if msg["role"] == "user" else "model"
                    chat_history.append({"role": role, "parts": [msg["content"]]})

                # Start chat with history
                chat = model.start_chat(history=chat_history)

                # Send the current message
                response = chat.send_message(prompt)

                # Display response
                st.markdown(response.text)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.caption("Built with Streamlit and Google Gemini API")
