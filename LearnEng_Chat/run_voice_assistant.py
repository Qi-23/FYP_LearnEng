# ../voice_samples/run_voice_assistant.py

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


def main(chat_history):
    """
    Main function to run the voice assistant.
    """
    chat_history.append({
        "role": "system",
        "content": """ You are a 27-year-old hotel staff member 
         called Joseph working at the hotel front desk. You are warm, welcoming, 
         patient, and highly professional, always eager to assist guests with their needs. 
         You take pride in delivering excellent customer service and ensures that 
         every guest feels comfortable and well-taken care of. 
         You will help the users with their booking room requests.
         Your answers are short and concise. """
    })

    # Generate an initial response from the assistant
    initial_response_api_key = get_response_api_key()
    initial_response_text = generate_response(Config.RESPONSE_MODEL, initial_response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
    logging.info(Fore.CYAN + "Initial Response: " + initial_response_text + Fore.RESET)

    # Append the assistant's initial response to the chat history
    chat_history.append({"role": "assistant", "content": initial_response_text})

    # Determine the output file format based on the TTS model
    if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
        initial_output_file = 'initial_output.mp3'
    else:
        initial_output_file = 'initial_output.wav'

    # Get the API key for TTS
    initial_tts_api_key = get_tts_api_key()

    # Convert the initial response text to speech and save it to the appropriate file
    text_to_speech(Config.TTS_MODEL, initial_tts_api_key, initial_response_text, initial_output_file, Config.LOCAL_MODEL_PATH)

    # Play the initial generated speech audio
    if Config.TTS_MODEL != "cartesia":
        play_audio(initial_output_file)

    # Clean up initial audio file
    delete_file(initial_output_file)

    while True:
        try:
            # Record audio from the microphone
            record_audio(Config.INPUT_AUDIO, timeout=30, phrase_time_limit=30)  

            
            transcription_api_key = get_transcription_api_key()
            
            
            user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)

            # Check if the transcription is empty or contains default phrases
            if not user_input or user_input.strip().lower() in ["thank you", "thanks", "thank you."]:
                logging.info("No valid transcription was returned. Starting recording again.")
                continue

            logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)

            # Phrases to end the chat
            exit_phrases = ["goodbye", "bye", "see you", "exit", "end"]
            if any(phrase in user_input.lower() for phrase in exit_phrases):
                chat_history.append({"role": "user", "content": user_input})
                break

            # Append the user's input to the chat history
            chat_history.append({"role": "user", "content": user_input})

            
            response_api_key = get_response_api_key()

            # Generate response
            response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
            logging.info(Fore.CYAN + "Response: " + response_text + Fore.RESET)

            # Append the assistant's response to the chat history
            chat_history.append({"role": "assistant", "content": response_text})

            # Determine the output file format based on TTS model
            if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
                output_file = 'output.mp3'
            else:
                output_file = 'output.wav'

            
            tts_api_key = get_tts_api_key()

            # Convert the response text to speech and save it to the appropriate file
            text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)

            # Play the generated speech audio
            if Config.TTS_MODEL != "cartesia":
                play_audio(output_file)
            
            # Clean up audio files
            delete_file(Config.INPUT_AUDIO)
            delete_file(output_file)

        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            delete_file(Config.INPUT_AUDIO)
            if 'output_file' in locals():
                delete_file(output_file)
            time.sleep(1)

if __name__ == "__main__":
    main()

# import logging
# import time
# from colorama import Fore, init
# from voice_assistant.audio import record_audio, play_audio
# from voice_assistant.transcription import transcribe_audio
# from voice_assistant.response_generation import generate_response
# from voice_assistant.text_to_speech import text_to_speech
# from voice_assistant.utils import delete_file
# from voice_assistant.config import Config
# from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

# from flask import Flask, render_template, request, jsonify
# import threading

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize colorama
# init(autoreset=True)

# # Flask app initialization
# app = Flask(__name__)

# # Chat history for the AI
# chat_history = [
#     {"role": "system", "content": """You are a 27-year-old hotel staff member 
#          called Joseph working at the hotel front desk. You are warm, welcoming, 
#          patient, and highly professional, always eager to assist guests with their needs. 
#          You take pride in delivering excellent customer service and ensures that 
#          every guest feels comfortable and well-taken care of."""}
# ]

# @app.route("/")
# def index():
#     return render_template('chatting.html')

# @app.route("/start_chat", methods=["GET"])
# def start_chat():
#     # AI's initial response
#     response = get_response("Hello! I'm your assistant. How can I help you today?")
#     return jsonify({"message": response})

# @app.route("/get", methods=["POST"])
# def get():
#     user_input = request.json['user_input']
#     logging.info(f"User input received: {user_input}")

#     # Check for exit phrases
#     exit_phrases = ["goodbye", "bye", "see you", "exit", "thank you", "end"]
#     if any(phrase in user_input.lower() for phrase in exit_phrases):
#         return jsonify({"message": "Goodbye! Have a great day!"})

#     # Continue chatting
#     response = get_response(user_input)
#     return jsonify({"message": response})

# def get_response(user_input):
#     try:
#         # Append user input to chat history
#         chat_history.append({"role": "user", "content": user_input})
        
#         # Generate a response using the AI
#         response_api_key = get_response_api_key()
#         response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
#         chat_history.append({"role": "assistant", "content": response_text})
        
#         # Start TTS for response
#         start_tts(response_text)
#         return response_text
#     except Exception as e:
#         logging.error(f"Error in generating response: {e}")
#         return "I'm sorry, there was an error in processing your request."

# def start_tts(response_text):
#     try:
#         # Convert text to speech and play audio
#         tts_api_key = get_tts_api_key()
#         text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, 'output.mp3', Config.LOCAL_MODEL_PATH)
#         play_audio('output.mp3')
#     except Exception as e:
#         logging.error(f"Error in TTS: {e}")

# if __name__ == "__main__":
#     app.run(debug=True)


