from colorama import Fore, init
from flask import Flask, render_template, request, jsonify
import threading
import logging
from flask_cors import CORS
from run_voice_assistant import initialize_chat, continue_chat, get_chat_status, update_chat_status, summarize_content, get_input, get_response, init_empty
import os
import json

from http.server import HTTPServer
import importlib

from dao.dbConnection import DBConnection
from controllers.scenario_controller import scenario_controller
from controllers.level_controller import level_controller
from model.scenario import Scenario
from model.level import Level

app = Flask(__name__)
CORS(app)

controllers_dir = './controllers'

for filename in os.listdir(controllers_dir):

    if filename.endswith('_controller.py'):
        module_name = f'controllers.{filename[:-3]}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'controller_blueprint'):
            app.register_blueprint(module.controller_blueprint, url_prefix=f'/{filename[:-14]}')

DBConnection.connect()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

chat_history = []  # Global variable for chat history

@app.route('/start_chat', methods=['POST'])
def start_chat():
    global chat_history
    chat_history = []
    data = request.json
    scenario_id = data.get('id')
    scenario = Scenario.fetch_by_id(scenario_id)

    initial_output_file = initialize_chat(scenario, chat_history)
    audio_name, audio_type = os.path.splitext(initial_output_file)
    return jsonify({"audio_name": audio_name, "audio_type": audio_type})

@app.route('/next_chat', methods=['POST'])
def next_chat():
    global chat_history
    global new_user_input
    global new_response

    output_file = continue_chat(chat_history)
    if output_file is not None:
        audio_name, audio_type = os.path.splitext(output_file)
        return jsonify({"audio_name": audio_name, "audio_type": audio_type})
    else:
        return jsonify({"audio_name": None, "audio_type": None})

@app.route('/empty', methods=['POST'])
def empty():
    global chat_history
    chat_history = []
    init_empty()
    return "success"

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    global chat_history
    return jsonify(chat_history)

@app.route('/get_user_input', methods=['GET'])
def get_user_input():
    new_user_input = get_input()
    return jsonify({'new_user_input': new_user_input})

@app.route('/get_new_response', methods=['GET'])
def get_new_response():
    new_response = get_response()
    return jsonify({'new_response': new_response})

@app.route('/get_status', methods=['GET'])
def get_status():
    status = get_chat_status()
    return jsonify({"chat_status": status})

@app.route('/update_status_to_ended', methods=['POST'])
def update_status_to_ended():
    global request_end
    global chat_history
    request_end = True

    if not chat_history:  
        update_chat_status("ended")
    else:
        update_chat_status("ended", chat_history)
      
    return jsonify("success")

@app.route('/get_summarized_content', methods=['GET'])
def get_summarized_content():
    global chat_history
    if not chat_history:
        response = summarize_content().get_json()
    else:
        response = summarize_content(chat_history).get_json()
    logging.info(Fore.CYAN + "Response: " + response['summarized_content'] + Fore.RESET)
    return response

def getScenarioInfo():
    try:
        scenarioID = request.args.get('id', type=int)
        scenario = Scenario.fetch_by_id(scenarioID)
        scenario = scenario.to_dict()
        return jsonify(scenario)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)