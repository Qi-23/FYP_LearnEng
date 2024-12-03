import logging
import time
from colorama import Fore, init
from voice_assistant.audio import record_audio, play_audio
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import generate_response
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.utils import delete_file
from voice_assistant.config import Config
from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

from flask import Flask, render_template, request, jsonify
import threading
import re

import subprocess
import webbrowser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama
init(autoreset=True)

app = Flask(__name__, static_url_path='/templates/chatting.html')

chat_history = [
    {"role": "system", "content": """ You are a 27-year-old hotel staff member 
     called Joseph working at the hotel front desk. You are warm, welcoming, 
     patient, and highly professional, always eager to assist guests with their needs. 
     You take pride in delivering excellent customer service and ensures that 
     every guest feels comfortable and well-taken care of. 
     You will help the users with their requests.
     Your answers are short and concise. """}
]

@app.route("/")
def index():
    return render_template('chatting.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = userInput()
        response = getResponse(user_input)
        startTTS(response)
        return jsonify({"user_input": user_input, "response": response})
    return "Method not allowed", 405

def userInput():
    try:
        record_audio(Config.INPUT_AUDIO)
        transcription_api_key = get_transcription_api_key()
        user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)
        if not user_input:
            logging.info("No transcription was returned. Starting recording again.")
            return None
        logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)
        if any(phrase in user_input.lower() for phrase in ["goodbye", "bye", "see you", "exit", "thank you", "end"]):
            return user_input
        chat_history.append({"role": "user", "content": user_input})
        return user_input
    except Exception as e:
        logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
        delete_file(Config.INPUT_AUDIO)
        time.sleep(1)
        return None

def getResponse(user_input):
    try:
        if user_input:
            response_api_key = get_response_api_key()
            response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
            chat_history.append({"role": "assistant", "content": response_text})
        else:
            response_text = "I'm sorry, I didn't catch your words. Could you say it again?"
        logging.info(Fore.CYAN + "Response: " + response_text + Fore.RESET)
        return filter_brackets(response_text)
    except Exception as e:
        logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
        delete_file(Config.INPUT_AUDIO)
        time.sleep(1)
        return None

def startTTS(response_text):
    try:
        if Config.TTS_MODEL in ['openai', 'elevenlabs', 'melotts', 'cartesia', 'deepgram']:
            output_file = 'output.mp3'
        else:
            output_file = 'output.wav'
        tts_api_key = get_tts_api_key()
        text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)
        if Config.TTS_MODEL != "deepgram":
            play_audio(output_file)
    except Exception as e:
        logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
        delete_file(Config.INPUT_AUDIO)
        if 'output_file' in locals():
            delete_file(output_file)
        time.sleep(1)

def filter_brackets(text):
    return re.sub(r'[\(\[].*?[\)\]]|\*.*?\*', '', text)

def initial_response():
    try:
        response_api_key = get_response_api_key()
        initial_response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
        logging.info(Fore.CYAN + "Initial Response: " + initial_response_text + Fore.RESET)
        chat_history.append({"role": "assistant", "content": initial_response_text})
        startTTS(initial_response_text)
        return initial_response_text
    except Exception as e:
        logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
        return None

if __name__ == "__main__":
    # Start the Flask app
    flask_process = subprocess.Popen(["python", "voice_assistant/main.py"])

    # Open the browser
    webbrowser.open("http://127.0.0.1:5000")

    # Ensure the process runs in the background
    flask_process.communicate()

    initial_response()
    app.run(debug=True)

# import logging
# import time
# from flask import Flask, render_template, redirect, url_for, jsonify
# import subprocess
# from voice_assistant.audio import record_audio, play_audio
# from voice_assistant.transcription import transcribe_audio
# from voice_assistant.response_generation import generate_response
# from voice_assistant.text_to_speech import text_to_speech
# from voice_assistant.utils import delete_file
# from voice_assistant.config import Config
# from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize Flask app
# app = Flask(__name__)

# # Chat history initialization
# chat_history = [
#     {"role": "system", "content": """ You are a 27-year-old hotel staff member 
#      called Joseph working at the hotel front desk. You are warm, welcoming, 
#      patient, and highly professional, always eager to assist guests with their needs. 
#      You take pride in delivering excellent customer service and ensure that 
#      every guest feels comfortable and well-taken care of. 
#      You will help the users with their requests.
#      Your answers are short and concise. """}
# ]

# # Route to serve the level_page.html
# @app.route("/")
# def level_page():
#     return render_template("level_page.html")

# # Route to handle the start of the chat
# @app.route("/start", methods=["GET", "POST"])
# def start_chatting():
#     # Start the Flask server subprocess for chatting
#     subprocess.Popen(["python", "voice_assistant/main.py"])
#     return redirect(url_for("chatting_page"))

# # Route to serve the chatting.html page
# @app.route("/chatting")
# def chatting_page():
#     return render_template("chatting.html")

# # Function to record user input and get the transcription
# def user_input():
#     try:
#         record_audio(Config.INPUT_AUDIO)  # Record audio

#         # Transcribe the audio
#         transcription_api_key = get_transcription_api_key()
#         user_input_text = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)

#         if user_input_text:
#             logging.info(f"You said: {user_input_text}")
#             if any(phrase in user_input_text.lower() for phrase in ["goodbye", "bye", "see you", "exit", "thank you", "end"]):
#                 return None  # End the chat if the user says goodbye
#             chat_history.append({"role": "user", "content": user_input_text})
#             return user_input_text
#         else:
#             logging.info("No transcription was returned. Starting recording again.")
#             return None

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         delete_file(Config.INPUT_AUDIO)
#         time.sleep(1)
#         return None

# # Function to generate AI response based on user input
# def get_response(user_input):
#     try:
#         if user_input:
#             response_api_key = get_response_api_key()
#             response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)

#             chat_history.append({"role": "assistant", "content": response_text})
#             return response_text
#         else:
#             return "I'm sorry, I didn't catch your words. Could you say it again?"

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         time.sleep(1)
#         return "Sorry, something went wrong. Please try again later."

# # Function to convert response text to speech
# def start_tts(response_text):
#     try:
#         output_file = 'output.mp3'
#         tts_api_key = get_tts_api_key()
#         text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)
#         play_audio(output_file)
#         delete_file(output_file)

#     except Exception as e:
#         logging.error(f"An error occurred during TTS: {e}")
#         delete_file(Config.INPUT_AUDIO)
#         time.sleep(1)

# # API route to interact with the AI and get a response
# @app.route("/get", methods=["GET", "POST"])
# def chat():
#     if request.method == "POST":
#         user_input_text = user_input()
#         if user_input_text is None:
#             return jsonify({"response": "Goodbye! Have a great day!"})

#         response = get_response(user_input_text)
#         start_tts(response)

#         return jsonify({"user_input": user_input_text, "response": response})

#     return "Method not allowed", 405

# if __name__ == "__main__":
#     # Start the Flask app on port 5000
#     app.run(debug=True)
