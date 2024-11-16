# server.py
from http.server import HTTPServer
import importlib
from flask import Flask
import os
from controllers.scenario_controller import scenario_controller  # Import user_controller blueprint
from controllers.user_controller import user_controller  # Import user_controller blueprint

app = Flask(__name__)

controllers_dir = './controllers'
# app.register_blueprint(scenario_controller, url_prefix='/scenario')
# app.register_blueprint(user_controller, url_prefix='/user')

for filename in os.listdir(controllers_dir):
  
    if filename.endswith('_controller.py'):
        module_name = f'controllers.{filename[:-3]}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'controller_blueprint'):
            # print(module.controller_blueprint)
            app.register_blueprint(module.controller_blueprint, url_prefix=f'/{filename[:-14]}')

if __name__ == '__main__':
    app.run(debug=True)