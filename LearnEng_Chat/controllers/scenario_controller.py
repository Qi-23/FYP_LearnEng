from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from flask import Flask, render_template, request, Blueprint, redirect, url_for, app, request, jsonify, send_file
import requests
from model.scenario import Scenario
from model.level import Level
from io import BytesIO
import imghdr
import base64
import logging

scenario_controller = Blueprint('scenario_controller', __name__)
controller_blueprint = scenario_controller

class ScenarioController(BaseHTTPRequestHandler):

    @classmethod
    def fetch_scenario_images(cls, scenario_id):
        try:
            scenario = Scenario.fetch_by_id(scenario_id)

            if not scenario:
                logging.error(f"Scenario with ID {scenario_id} not found")
                return {
                    "scenarioImage": None,
                    "backgroundImage": None,
                    "scenarioImageType": None,
                    "backgroundImageType": None
                }

            image_data = {}
            scenarioImage_type = None
            backgroundImage_type = None

            if scenario._image:
                scenarioImage_type = imghdr.what(None, h=scenario._image) or 'jpeg'
                image_data['scenarioImage'] = base64.b64encode(BytesIO(scenario._image).getvalue()).decode('utf-8')
            else:
                image_data['scenarioImage'] = None

            if scenario._backgroundImage:
                backgroundImage_type = imghdr.what(None, h=scenario._backgroundImage) or 'jpeg'
                image_data['backgroundImage'] = base64.b64encode(BytesIO(scenario._backgroundImage).getvalue()).decode('utf-8')
            else:
                image_data['backgroundImage'] = None

            return {
                "scenarioImage": image_data['scenarioImage'],
                "backgroundImage": image_data['backgroundImage'],
                "scenarioImageType": f"image/{scenarioImage_type}" if image_data['scenarioImage'] else None,
                "backgroundImageType": f"image/{backgroundImage_type}" if image_data['backgroundImage'] else None
            }

        except Exception as e:
            logging.error(f"Error fetching images for scenario {scenario_id}: {str(e)}")
            return {
                "scenarioImage": None,
                "backgroundImage": None,
                "scenarioImageType": None,
                "backgroundImageType": None
            }

    @scenario_controller.route('/', methods=['GET'])
    def scenarioList():
        try:
            scenarios = Scenario.fetch_all()
            scenarios_dict = []

            for scenario in scenarios:
                try:
                    scenario_data = scenario.to_dict()

                    image_data = ScenarioController.fetch_scenario_images(scenario._id)
                    scenario_data.update(image_data)

                    scenarios_dict.append(scenario_data)
                        
                except Exception as e:
                    logging.error(f"Error fetching images for scenario {scenario._id}: {str(e)}")
                    scenario_data.update({
                        "scenarioImage": None,
                        "backgroundImage": None,
                        "scenarioImageType": None,
                        "backgroundImageType": None
                    })

            return jsonify(scenarios_dict)
       
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @scenario_controller.route('/submit_scenario', methods=['POST'])
    def submit_scenario():
        try:
            scenarioID = request.form['scenarioID']
            # scenarioImage = request.form['scenarioImage']
            scenarioName = request.form['scenarioName']
            scenarioDesc = request.form['scenarioDescription']
            characterDesc = request.form['characterDescription']
            vocab = request.form['vocab']
            grammar = request.form['grammar']
            situationalChat = request.form['situationalChat']
            characterFileName = request.form['characterFileName']
            # backgroundImage = request.form['backgroundImage']
            level = request.form['level']
            
            scenarioImage = request.files.get('scenarioImage')
            backgroundImage = request.files.get('backgroundImage')
            scenarioImage = scenarioImage.read() if scenarioImage else None
            backgroundImage = backgroundImage.read() if backgroundImage else None

            print(scenarioID)
            try:
                if(scenarioID):
                    # update scenario details
                    scenario = Scenario(scenarioName, scenarioDesc, characterDesc, vocab, characterFileName, grammar, situationalChat, level, scenarioID, scenarioImage, backgroundImage)
                    # print(scenario)
                    scenario.update_scenario()
                else: 
                    # create new scenario
                    scenario = Scenario(scenarioName, scenarioDesc, characterDesc, vocab, characterFileName, grammar, situationalChat, level, scenarioImage, backgroundImage)
                    # print(scenario)
                    scenario.create_scenario()
                
                return jsonify({"message": "Scenario created successfully"}), 200
        
            except Exception as e:
                logging.error(f"Error creating/updating scenario: {str(e)}")
                return jsonify({"error": str(e)}), 500

        except Exception as e:
            logging.error(f"Error in submit_scenario: {str(e)}")
            return jsonify({"error": str(e)}), 500
            
    @scenario_controller.route('/get_scenario_info', methods=['GET'])
    def getScenarioInfo():
        try:
            scenarioID = request.args.get('id', type=int)
            scenario = Scenario.fetch_by_id(scenarioID)
            scenario = scenario.to_dict()
            return jsonify(scenario)
       
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @scenario_controller.route('/delete_scenario', methods=['POST'])
    def delete_scenario():
        try:
            scenarioID = request.json.get('id')
            if not scenarioID:
                return jsonify({"error": "Scenario ID is required"}), 400

            Scenario.delete_by_id(scenarioID)

            logging.info(f"Deleted scenario with ID: {scenarioID}")
            return jsonify({"message": "Scenario deleted successfully"}), 200

        except Exception as e:
            logging.error(f"Error deleting scenario: {str(e)}")
            return jsonify({"error": str(e)}), 500
        
    @scenario_controller.route('/images/<int:scenario_id>', methods=['GET'])
    def get_scenario_images(scenario_id):
        try:
            scenario = Scenario.fetch_by_id(scenario_id)

            if not scenario:
                logging.error(f"Scenario with ID {scenario_id} not found")
                return jsonify({"error": "Scenario not found"}), 404
            
            image_data = {}
            scenarioImage_type = None
            backgroundImage_type = None

            if scenario._image:
                scenarioImage_type = imghdr.what(None, h=scenario._image) or 'jpeg'
                image_data['scenarioImage'] = BytesIO(scenario._image)
            else:
                image_data['scenarioImage'] = None

            if scenario._backgroundImage:
                backgroundImage_type = imghdr.what(None, h=scenario._backgroundImage) or 'jpeg'
                image_data['backgroundImage'] = BytesIO(scenario._backgroundImage)
            else:
                image_data['backgroundImage'] = None
            
            return jsonify({
                "scenarioImage": base64.b64encode(image_data['scenarioImage'].getvalue()).decode('utf-8') if image_data['scenarioImage'] else None,
                "backgroundImage": base64.b64encode(image_data['backgroundImage'].getvalue()).decode('utf-8') if image_data['backgroundImage'] else None,
                "scenarioImageType": f"image/{scenarioImage_type}" if image_data['scenarioImage'] else None ,
                "backgroundImageType": f"image/{backgroundImage_type}" if image_data['backgroundImage'] else None 
            })
        
        except Exception as e:
            logging.error(f"Error fetching images for scenario {scenario_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
     
    def process_scenario_update(self):
        return