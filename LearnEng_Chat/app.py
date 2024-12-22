# server.py
from http.server import HTTPServer
import importlib
from flask import Flask, jsonify
from flask_cors import CORS
import os

from dao.dbConnection import DBConnection
from controllers.scenario_controller import scenario_controller  # Import scenario_controller blueprint

# import the classes / model
from model.level import Level
from model.scenario import Scenario
from model.editor import Editor
from model.voice import Voice
from model.virtualCharacter import VirtualCharacter
from model.learner import Learner
from model.learnerScenario import LearnerScenario
from model.summary import Summary

app = Flask(__name__)
CORS(app)

controllers_dir = './controllers'

for filename in os.listdir(controllers_dir):
  
    if filename.endswith('_controller.py'):
        module_name = f'controllers.{filename[:-3]}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'controller_blueprint'):
            # print(module.controller_blueprint)
            app.register_blueprint(module.controller_blueprint, url_prefix=f'/{filename[:-14]}')

DBConnection.connect()

# @app.route("/api/chat", methods=['GET'])
# def return_chat(): 
#     return jsonify({
#         'tts_audio_name' : 'response'
#     })

# @app.route("/api/home", methods=['GET'])
# def return_home():
#     return jsonify({'message': "response"})


# testing start here -------------------------------------------------------------------------------

# try run (change the class name to test)
# result_one = Voice.fetch_by_id(1)
# result_all = Voice.fetch_all()
# i = 0
# print()
# for each in result_all:
#     print(each)
#     print()

# print(f"\n{result_one}\n")




# Flask connection
if __name__ == '__main__':
    app.run(debug=True)