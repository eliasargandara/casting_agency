import traceback
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException, InternalServerError
from marshmallow import ValidationError

errors_blueprint = Blueprint('errors', __name__)


@errors_blueprint.app_errorhandler(ValidationError)
def validation_error(exception):
    invalid_params = []

    def traverse_messages(attribute, messages):
        if type(messages) is list:
            for message in messages:
                invalid_params.append({
                    'name': attribute,
                    'reason': message
                })
        else:
            for subattribute, submessages in messages.items():
                if type(subattribute) is int:
                    traverse_messages(
                        f'{attribute}[{subattribute}]',
                        submessages
                    )
                else:
                    new_attribute = None
                    if attribute:
                        new_attribute = f'{attribute}.{subattribute}'
                    else:
                        new_attribute = f'{subattribute}'

                    traverse_messages(
                        new_attribute,
                        submessages
                    )

    traverse_messages('', exception.messages)

    return jsonify({
        'success': False,
        'description': 'The request parameters are not valid.',
        'invalid_params': invalid_params
    }), 400

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
    print(trace)
    return jsonify({
        'success': False,
        'description': (
            'We apoligize. Our service seems to'
            ' have experienced an unexpected error.'
        )
    }), 500
