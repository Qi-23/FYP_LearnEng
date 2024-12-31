# controllers/level_controller.py

from flask import Blueprint, jsonify, request
from model.editor import Editor

editor_controller = Blueprint('editor_controller', __name__)
controller_blueprint = editor_controller

@editor_controller.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        authorized = Editor.check_authentication(username, password)

        return jsonify({"authorized": authorized}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500