from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from flask import Flask, render_template, request, Blueprint, redirect, url_for, app, request, jsonify
import requests
from model.scenario import Scenario
from model.level import Level

scenario_controller = Blueprint('scenario_controller', __name__)
controller_blueprint = scenario_controller

class ScenarioController(BaseHTTPRequestHandler):
    @scenario_controller.route('/scenario_configuration', methods=['GET'])
    def scenarioConfiguration():
        scenarioID = request.args.get('id', type=int)
        level = request.args.get('level', type=int)
        print(scenarioID)
        print(level)
        # to find the scenario details

        if(scenarioID):
            scenario = Scenario.fetch_by_id(scenarioID)
            process = "loadScenario"
            scenario = scenario.to_dict()

            print(scenario)

            payload = {
                "process": process,
                "scenario": scenario
            }

            api_endpoint = "http://localhost:5137/api/ScenarioConfig"

            try:
                response = requests.post(api_endpoint, json=payload)
                if response.status_code == 200:
                    return redirect("http://localhost:5137/scenario_configuration.html")
                else:
                    return jsonify({"error": f"Failed to post scenario, status code: {response.status_code}"}), response.status_code
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        elif (level is not None):
            process = "addScenario"
            level = {
                "id": level
            }

            payload = {
                "process": process,
                "level": level
            }

            api_endpoint = "http://localhost:5137/api/ScenarioConfig"

            try:
                response = requests.post(api_endpoint, json=payload)
                if response.status_code == 200:
                    return redirect("http://localhost:5137/scenario_configuration.html")
                else:
                    return jsonify({"error": f"Failed to post scenario, status code: {response.status_code}"}), response.status_code
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        else :
            return render_template('scenario_configuration.html')
       
       
    @scenario_controller.route('/', methods=['GET'])
    def scenarioList():
        try:
            scenarios = Scenario.fetch_all() # all scenario object
            api_endpoint = "http://localhost:5137/api/ScenarioConfig"
            requests.post(api_endpoint, json={})

            scenarios_dict = [s.to_dict() for s in scenarios]
            return jsonify(scenarios_dict)
            
            # return render_template('editor_scenario_page.html', scenarios=scenarios)
       
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @scenario_controller.route('/submit_scenario', methods=['POST'])
    def submit_scenario():
        print(request.form)
        scenarioID = request.form['scenarioID']
        scenarioImage = request.form['scenarioImage']
        scenarioName = request.form['scenarioName']
        scenarioDesc = request.form['scenarioDescription']
        characterDesc = request.form['characterDescription']
        vocab = request.form['vocab']
        grammar = request.form['grammar']
        situationalChat = request.form['situationalChat']
        characterFileName = request.form['characterFileName']
        backgroundImage = request.form['backgroundImage']
        level = request.form['level']

        print(scenarioID)
        try:
            if(scenarioID):
                # update scenario details
                scenario = Scenario(scenarioName, scenarioImage, scenarioDesc, characterDesc, vocab, characterFileName, backgroundImage, grammar, situationalChat, level, scenarioID)
                print(scenario)
                scenario.update_scenario()
            else: 
                # create new scenario
                scenario = Scenario(scenarioName, scenarioImage, scenarioDesc, characterDesc, vocab, characterFileName, backgroundImage, grammar, situationalChat, level)
                print(scenario)
                scenario.create_scenario()
            
            return jsonify({"message": "Scenario created successfully"}), 200
       
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    @scenario_controller.route('/get_scenario_info', methods=['GET'])
    def getScenarioInfo():
        try:
            scenarioID = request.args.get('id', type=int)
            scenario = Scenario.fetch_by_id(scenarioID)
            scenario = {
                "id": scenario._id,
                "name": scenario._name,
                "image": scenario._image,
                "scenarioDesc": scenario._scenarioDesc,
                "characterDesc": scenario._characterDesc,
                "vocab": scenario._vocab,
                "grammar": scenario._grammar,
                "situationalChat": scenario._situationalChat,
                "characterFileName": scenario._characterFileName,
                "backgroundImage": scenario._backgroundImage,
                "level": scenario._level._id
            }
            return jsonify(scenario)
       
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def process_scenario_update(self):
        return
