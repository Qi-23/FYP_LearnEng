# controllers/level_controller.py

from flask import Blueprint, jsonify
from model.level import Level

level_controller = Blueprint('level_controller', __name__)
controller_blueprint = level_controller

@level_controller.route('/', methods=['GET'])
def get_all_levels():
    try:
        levels = Level.fetch_all()
        levels_dict = [l.to_dict() for l in levels]
        return jsonify(levels_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@level_controller.route('/<int:level_id>')
def get_level(level_id):
    try:
        level = Level.fetch_by_id(level_id)
        if level:
            return jsonify(level.to_dict())
        else:
            return jsonify({"error": "Level not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500