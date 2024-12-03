from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from flask import Flask, render_template, request, Blueprint, redirect, url_for, app
from model.scenario import Scenario
from model.level import Level

scenario_controller = Blueprint('scenario_controller', __name__)
controller_blueprint = scenario_controller

class ScenarioController(BaseHTTPRequestHandler):
    @scenario_controller.route('/scenario_configuration', methods=['GET'])
    def scenarioConfiguration():
        scenarioID = request.args.get('id', type=int)
        # to find the scenario details

        if(scenarioID):
            print("find the scenario details")
        else:
            return render_template('scenario_configuration.html')
       
        # else:
        #     self.send_response(404)
        #     self.end_headers()
        #     self.wfile.write(b"Page not found.")

    @scenario_controller.route('/submit_scenario', methods=['POST'])
    def submit_scenario():
        scenarioID = request.form['scenarioID']
        scenarioImage = request.form['scenarioImage']
        scenarioName = request.form['scenarioName']
        scenarioDesc = request.form['scenarioDescription']
        characterDesc = request.form['characterDescription']
        vocab = request.form['vocab']
        level = request.form['level']

        if(scenarioID):
            # update scenario details
            print("with id")
        else: 
            # create new scenario
            scenario = Scenario(scenarioName, scenarioImage, scenarioDesc, characterDesc, vocab, level)
            print(scenario)
            scenario.create_scenario()

        return render_template('scenario_configuration.html')
    

    def process_scenario_update(self):
        return
