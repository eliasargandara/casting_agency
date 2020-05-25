from flask import Blueprint, jsonify

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/health')
def health():
    return jsonify({
        'success': True
    })
