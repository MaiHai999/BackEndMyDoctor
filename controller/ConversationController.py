from BackEnd.source.entity.MyConnectPro import MyConnectPro
from BackEnd.source.services.models import *
from BackEnd.source.controller.LLMController import LLMController

from BackEnd.source.entity.MyConnectPro import EntityHandler
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required


from flask import Blueprint
from flask import request , stream_with_context
from flask import jsonify
import os

con_blueprint = Blueprint('conversation', __name__)

#khởi tạo session
user = os.environ.get('tk_user')
password_db = os.environ.get('password_tk_user')
db_manager = MyConnectPro(user, password_db)
db_manager.connect()
session = db_manager.get_session()

#khởi tạo llm
base_url = os.environ.get('base_url')
LLM = LLMController(base_url)


@con_blueprint.route('/conversation', methods=["GET"])
@jwt_required()
def get_all_conversation():
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
            if conversation.status != 0:
                conversation_list.append(conversation_dict)

        return jsonify(conversation_list), 200

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500
def check_conversation(id_user , id_conversation):
    check = False
    user = EntityHandler.get_entity_id(session, User, id_user)
    for conversation in user.conversations:
         if conversation.id == int(id_conversation):
            check = True
            return check

    return check

@con_blueprint.route('/message', methods=["GET"])
@jwt_required()
def get_message():
    try:
        identity = get_jwt_identity()
        id_user = identity['id_user']
        id_conversation = request.args.get('id_conversation')
        if check_conversation(id_user , id_conversation):
            conversations = EntityHandler.get_entity_id(session , Conversation , id_conversation)
            message_list = []
            for mess in conversations.messages:
                message_dict = {
                    'id': mess.id,
                    'human': mess.human,
                    'create_date': mess.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'ai': mess.ai

                }
                message_list.append(message_dict)
            return jsonify(message_list), 200

        else:
            response = jsonify({"mes": "Access denied to the data."})
            return response, 403

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

@con_blueprint.route('/del_con', methods=["GET"])
@jwt_required()
def delete():
    try:
        identity = get_jwt_identity()
        id_user = identity['id_user']
        id_conversation = int(request.args.get('id_conversation'))
        if check_conversation(id_user, id_conversation):
            is_successfully = EntityHandler.update_status(session , Conversation , id_conversation , 0)
            if is_successfully:
                response = jsonify({"msg": "Delete conversation successfully"})
                return response, 200
            else:
                response = jsonify({"error": "Internal Server Error"})
                return response, 500

        else:
            response = jsonify({"mes": "Access denied to the data."})
            return response, 403


    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500


@con_blueprint.route('/chat', methods=["GET"])
@jwt_required()
def chat():
    human_message = request.args.get('human')
    return stream_with_context(LLM.query_message(human_message))



























