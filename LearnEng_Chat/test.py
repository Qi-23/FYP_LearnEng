# test.py

from flask import Flask, render_template, request, jsonify
import threading
import logging
from run_voice_assistant import main as run_voice_assistant

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to store chat history
chat_history = []

@app.route('/')
def index():
    return render_template('chatting.html')

@app.route('/start_chat', methods=['POST'])
def start_chat():
    global chat_history
    chat_history = []
    threading.Thread(target=run_voice_assistant, args=(chat_history,)).start()
    return jsonify({"status": "Chat started"})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    global chat_history
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)