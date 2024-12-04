# test.py

from flask import Flask, render_template, request, jsonify
import threading
import logging
from flask_cors import CORS
from run_voice_assistant import initialize_chat, continue_chat, get_chat_status, update_chat_status
import os

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to store chat history
chat_history = []

# @app.route('/')
# def index():
#     return render_template('chatting.html')

from colorama import Fore, init

@app.route('/start_chat', methods=['POST'])
def start_chat():
    global chat_history
    chat_history = []
    initial_output_file = initialize_chat(chat_history, )
    logging.info(Fore.GREEN + "Initial: " + initial_output_file)
    audio_name, audio_type = os.path.splitext(initial_output_file)
    return jsonify({"audio_name": audio_name, "audio_type" : audio_type})
    
@app.route('/next_chat', methods=['POST'])
def next_chat():
    global chat_history
    output_file = continue_chat(chat_history, )
    logging.info(Fore.GREEN + "Response: " + output_file)
    audio_name, audio_type = os.path.splitext(output_file)
    return jsonify({"audio_name": audio_name, "audio_type" : audio_type})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    global chat_history
    return jsonify(chat_history)

@app.route('/get_status', methods=['GET'])
def get_status():
    status = get_chat_status()
    return jsonify({"chat_status" : status})

@app.route('/update_status_to_none', methods=['POST'])
def update_status_to_none():
    update_chat_status("none")
    return jsonify("success")

if __name__ == '__main__':
    app.run(debug=True)