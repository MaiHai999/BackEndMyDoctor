from BackEnd.source.entity.MyConnectPro import MyConnectPro
from BackEnd.source.services.models import *

from BackEnd.source.entity.MyConnectPro import EntityHandler

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import NoResultFound

from flask import Blueprint
from flask import request
import json
from flask import jsonify
import os

con_blueprint = Blueprint('conversation', __name__)

user = os.environ.get('tk_user')
password_db = os.environ.get('password_tk_user')
db_manager = MyConnectPro(user, password_db)
db_manager.connect()
session = db_manager.get_session()


@con_blueprint.route('/get_conversation', methods=["GET"])
@jwt_required()
def get_conversation():
    try:
        identity = get_jwt_identity()
        id_user = identity['id_user']
        user = EntityHandler.get_entity_id(session , User , id_user)
        conversation_list = []
        for conversation in user.conversations:
            conversation_dict = {
                'id': conversation.id,
                'title': conversation.title,
                'create_date': conversation.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                'id_user': conversation.id_user,
                'status': conversation.status
            }
            conversation_list.append(conversation_dict)

        return jsonify(conversation_list), 200
    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500
