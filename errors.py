import traceback
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException, InternalServerError

errors_blueprint = Blueprint('errors', __name__)

@errors_blueprint.app_errorhandler(HTTPException)
def handle_exception(exception):
    return jsonify({
        'success': False,
        'description': exception.description
    }), exception.code

@errors_blueprint.app_errorhandler(InternalServerError)
@errors_blueprint.app_errorhandler(Exception)
def internal_error(exception):
    trace = traceback.format_exc()
    return jsonify({
        'success': False,
        'description': (
            'We apoligize. Our service seems to'
            ' have experienced an unexpected error.'
        )
    }), 500
