# ../voice_samples/run_voice_assistant.py

import logging
import time
from flask import jsonify 
from colorama import Fore, init
from voice_assistant.audio import record_audio, play_audio
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import generate_response
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.utils import delete_file
from voice_assistant.config import Config
from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

import json


status = "none"
new_user_input = ""
new_response = ""

# def initialize_chat(chat_history):
#     global status
#     global new_response
#     global new_user_input
#     new_user_input = ""
#     new_response = ""

#     status = "processing"

#     keywords = ["booking", "room", "check-in", "check-out", "reservation", "guest", "confirmation", "details", "availability", "facility"]

#     chat_history.append({
#         "role": "system",
#         "content": f""" You are a 27-year-old hotel staff member 
#          called Joseph working at the hotel front desk in physical hotel. You are warm, welcoming, 
#          patient, and highly professional, always eager to assist guests with their needs. 
#          You take pride in delivering excellent customer service and ensure that 
#          every guest feels comfortable and well-taken care of. 
#          You will help the users with their booking room requests.
#          Your answers are very very very short and concise.
#          Try to use these keywords when responding: {', '.join(keywords)}."""
#     })

#     # Generate an initial response from the assistant
#     initial_response_api_key = get_response_api_key()
#     new_response = initial_response_text = generate_response(Config.RESPONSE_MODEL, initial_response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
#     logging.info(Fore.CYAN + "Initial Response: " + initial_response_text + Fore.RESET)

#     # Append the assistant's initial response to the chat history
#     chat_history.append({"role": "assistant", "content": initial_response_text})

#     # Determine the output file format based on the TTS model
#     initial_output_file_name = 'initial_output.mp3'
#     initial_output_file = '../learneng_vite/public/audios/' + initial_output_file_name

#     # Get the API key for TTS
#     initial_tts_api_key = get_tts_api_key()

#     # Convert the initial response text to speech and save it to the appropriate file
#     text_to_speech(Config.TTS_MODEL, initial_tts_api_key, initial_response_text, initial_output_file, Config.LOCAL_MODEL_PATH)

#     return initial_output_file_name

# def continue_chat(chat_history):
#     try:
#         global status
#         global new_user_input
#         global new_response

#         status = "talking"

#         # Record audio from the microphone
#         record_audio(Config.INPUT_AUDIO, timeout=30, phrase_time_limit=30)  

#         status = "processing"
#         transcription_api_key = get_transcription_api_key()
        
#         new_user_input = user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)

#         # Check if the transcription is empty or contains default phrases
#         if not user_input or user_input.strip().lower() in ["thank you", "thanks", "thank you."]:
#             logging.info("No valid transcription was returned. Starting recording again.")
#             return

#         logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)

#         # Phrases to end the chat
#         exit_phrases = ["goodbye", "bye", "see you", "exit", "end"]
#         if any(phrase in user_input.lower() for phrase in exit_phrases):
#             chat_history.append({"role": "user", "content": user_input})
#             return

#         # Append the user's input to the chat history
#         chat_history.append({"role": "user", "content": user_input})

#         # Keywords for the AI to prioritize in its responses
#         keywords = ["booking", "room", "check-in", "check-out", "reservation", "guest", "confirmation", "details", "availability", "amenities"]

#         response_api_key = get_response_api_key()

#         # Generate response
#         response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)

#         # Attempt to integrate keywords dynamically into the response
#         # for keyword in keywords:
#         #     if keyword not in response_text.lower():
#         #         response_text += f" {keyword}."

#         logging.info(Fore.CYAN + "Response: " + response_text + Fore.RESET)

#         new_response = response_text

#         # Append the assistant's response to the chat history
#         chat_history.append({"role": "assistant", "content": response_text})

#         # Determine the output file format based on TTS model
#         output_file_name = 'output.mp3'
#         output_file = '../learneng_vite/public/audios/' + output_file_name
#         tts_api_key = get_tts_api_key()

#         # Convert the response text to speech and save it to the appropriate file
#         text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)

#         # Clean up audio files
#         delete_file(Config.INPUT_AUDIO)

#         status = "none"
#         return output_file_name

#     except Exception as e:
#         logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
#         delete_file(Config.INPUT_AUDIO)
#         if 'output_file' in locals():
#             delete_file(output_file)
#         time.sleep(1)


def initialize_chat(chat_history):
    global status
    global new_response
    global new_user_input
    new_user_input = ""
    new_response = ""

    status = "processing"
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
         Your answers are short and concise.
         Your answers are very very very short and concise. """
    })

    # Generate an initial response from the assistant
    initial_response_api_key = get_response_api_key()
    new_response = initial_response_text = generate_response(Config.RESPONSE_MODEL, initial_response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
    logging.info(Fore.CYAN + "Initial Response: " + initial_response_text + Fore.RESET)

    # Append the assistant's initial response to the chat history
    chat_history.append({"role": "assistant", "content": initial_response_text})

    # Determine the output file format based on the TTS model
    if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
        initial_output_file_name = 'initial_output.mp3'
    else:
        initial_output_file_name = 'initial_output.mp3'

    initial_output_file = '../learneng_vite/public/audios/' + initial_output_file_name

    # Get the API key for TTS
    initial_tts_api_key = get_tts_api_key()

    # Convert the initial response text to speech and save it to the appropriate file
    text_to_speech(Config.TTS_MODEL, initial_tts_api_key, initial_response_text, initial_output_file, Config.LOCAL_MODEL_PATH)

    # Play the initial generated speech audio
    # if Config.TTS_MODEL != "cartesia":
    #     play_audio(initial_output_file)

    # Clean up initial audio file
    # delete_file(initial_output_file)
    
    return initial_output_file_name

def continue_chat(chat_history):
    try:
        global status
        global new_user_input
        global new_response

        status = "talking"
        # Record audio from the microphone
        record_audio(Config.INPUT_AUDIO, timeout=30, phrase_time_limit=30)  

        status = "processing"
        transcription_api_key = get_transcription_api_key()
        
        new_user_input = user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)

        # Check if the transcription is empty or contains default phrases
        if not user_input or user_input.strip().lower() in ["thank you", "thanks", "thank you."]:
            logging.info("No valid transcription was returned. Starting recording again.")
            # continue

        # new_user_input = user_input
        logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)

        # Phrases to end the chat
        exit_phrases = ["goodbye", "bye", "see you", "exit", "end"]
        if any(phrase in user_input.lower() for phrase in exit_phrases):
            chat_history.append({"role": "user", "content": user_input})
            # break
            return

        # Append the user's input to the chat history
        chat_history.append({"role": "user", "content": user_input})

        
        response_api_key = get_response_api_key()

        # Generate response
        new_response = response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
        logging.info(Fore.CYAN + "Response: " + response_text + Fore.RESET)

        # new_response = response_text

        # Append the assistant's response to the chat history
        chat_history.append({"role": "assistant", "content": response_text})

        # Determine the output file format based on TTS model
        if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
            output_file_name = 'output.mp3'
        else:
            output_file_name = 'output.mp3'

        output_file = '../learneng_vite/public/audios/' + output_file_name
        tts_api_key = get_tts_api_key()

        # Convert the response text to speech and save it to the appropriate file
        text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)

        # Play the generated speech audio
        # if Config.TTS_MODEL != "cartesia":
        #     play_audio(output_file)
        
        # Clean up audio files

        delete_file(Config.INPUT_AUDIO)
        # delete_file(output_file)

        status = "none"
        return output_file_name

    except Exception as e:
        logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
        delete_file(Config.INPUT_AUDIO)
        if 'output_file' in locals():
            delete_file(output_file)
        time.sleep(1)

def get_chat_status() :
    global status
    return status

def update_chat_status(new_status) :
    global status
    status = new_status

def get_input() :
    global new_user_input
    return new_user_input

def get_response() :
    global new_response
    return new_response

def init_empty() : 
    global status
    global new_user_input
    global new_response
    status = ""
    new_response = ""
    new_user_input = ""

def summarize_content(chat_history = None):
    try:
        global status
        status = "summarizing"
        
        file_path = "../learneng_vite/public/audios/"

        chat_history_file = file_path + "chat_history.json"

        with open(chat_history_file, "r") as file:
            chat_history = json.load(file)

        if(chat_history):
            filtered_chat_history = [item for item in chat_history if item.get("role") != "system"]
            with open(chat_history_file, "w") as file:
                json.dump(filtered_chat_history, file)
                print(f"Content saved to {chat_history_file}")
    
        summarizing_history = [
            {
                "role": "system",
                "content": """ Summarize the performance of role user only in term of their grammar mistake according to this conversation. Strictly follow the format as shown below.
                 Use the format as below :
                 Grammar mistakes:
                 1. **Type of mistake**
                 * "Sentence of user role with mistake."
                    Correction: "Corrected version of the sentence"
                    Note: "Grammar fixing note."

                 2. **Type of mistake**
                 * "Sentence of user role with mistake."
                    Correction: "Corrected version of the sentence"
                    Note: "Grammar fixing note."
                    
                 ...
                  
                 Example of response: 
                  **Grammar Mistakes:**

                 1. **Subject-Verb Agreement**
                 * "Hi, I like to books a room for two night."
                 * Correction: "Hi, I would like to book a room for two nights."
                 * Note: "The subject 'I' requires the correct modal verb 'would like,' and 'books' should be the base form 'book.' Additionally, 'nights' should be plural for grammatical agreement."

                 2. **Verb-Subject Agreement**
                 * "Is just me and my friend."
                 * Correction: "It is just me and my friend."
                 * Note: "The sentence lacks the subject 'It,' which is required to form a complete and grammatically correct sentence."

                 3. **Word Choice**
                 * "Non smoke and mountain view if you have it."
                 * Correction: "Non-smoking and a mountain view, if available."
                 * Note: "The phrase 'Non smoke' should be 'Non-smoking,' and 'if you have it' is more appropriately rephrased as 'if available' for clarity and conciseness."

                 4. **Missing Article**
                 * "I'm Sarah Lee, and my phone 987654."
                 * Correction: "I'm Sarah Lee, and my phone number is 987654."
                 * Note: "The article 'number' is missing after 'phone,' and the verb 'is' is needed to complete the sentence."

                 5. **Incorrect Preposition**
                 * "That's great, thank for help me!"
                 * Correction: "That's great, thank you for helping me!"
                 * Note: "The preposition 'for' is required after 'thank,' and the correct phrase is 'helping me' instead of 'help me' to match the intended context." """
            }
        ]

        # Combine the assistant and user conversations into one content
        combined_content = ""
        for entry in chat_history:
            if entry["role"] in ["assistant", "user"]:
                combined_content += f"{entry['role'].capitalize()}: {entry['content']}\n"

        # Add the combined content to the system's content in summarizing_history
        summarizing_history.append({
            "role": "system",
            "content": combined_content
        })

        summarizing_content_file = file_path + "save.json"
        with open(summarizing_content_file, "w") as file:
            json.dump(summarizing_history, file)

        try:
            response_api_key = get_response_api_key()

            # Generate response
            response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, summarizing_history, Config.LOCAL_MODEL_PATH)
            response_text = response_text.replace("role user", "learner")
            response_text = response_text.replace("user", "learner")
            response_text = response_text.replace("User", "Learner")
        
            # output_file_name = 'output.mp3'
            # audio_output_file = '../learneng_vite/public/audios/' + output_file_name

            # tts_api_key = get_tts_api_key()

            # # Convert the response text to speech and save it to the appropriate file
            # text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, audio_output_file, Config.LOCAL_MODEL_PATH)

            status = "none"

        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            time.sleep(1)

        summarized_content_file = file_path + "summarizedContent.json"

        with open(summarized_content_file, "w") as file:
            json.dump(response_text, file)
            print(f"Content saved to {summarized_content_file}")

        # return jsonify({"summarized_content" : response_text, "audio_file" : audio_output_file})
        return jsonify({"summarized_content" : response_text})
    except Exception as e:
        logging.error(Fore.RED + f"An error occurred, unable to read file: {e}" + Fore.RESET)

