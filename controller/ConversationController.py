from BackEnd.source.entity.MyConnectPro import MyConnectPro
from BackEnd.source.services.models import *
from BackEnd.source.controller.LLMController import LLMController
from BackEnd.source.Config import limiter

from BackEnd.source.entity.MyConnectPro import EntityHandler
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

from datetime import datetime
from functools import wraps
from flask import Blueprint
from flask import request , stream_with_context
from flask import jsonify
import os
from sqlalchemy.exc import IntegrityError


con_blueprint = Blueprint('conversation', __name__)
#lấy limiter


#khởi tạo session
user = os.environ.get('tk_user')
password_db = os.environ.get('password_tk_user')
db_manager = MyConnectPro(user, password_db)
db_manager.connect()
session = db_manager.get_session()

#khởi tạo llm
base_url = os.environ.get('base_url')
# LLM = LLMController(base_url)


@con_blueprint.route('/conversation', methods=["GET"])
@jwt_required()
# @limiter.limit("30 per 15 minutes")
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
# @limiter.limit("70 per 15 minutes")
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
# @limiter.limit("70 per 15 minutes")
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
@limiter.limit("10 per minute")
def chat():
    try:
        human_message = request.args.get('human')
        streamed_data = LLM.query_message(human_message)
        return stream_with_context(streamed_data), 200
    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500


@con_blueprint.route('/save', methods=["GET"])
@jwt_required()
# @limiter.limit("10 per minute")
def save_conversation():
    try:
        identity = get_jwt_identity()
        id_user = identity['id_user']
        human_message = request.args.get('human')
        ai_message = request.args.get('ai')

        try:
            new_conversation = Conversation()
            id = EntityHandler.generative_ID(session, Conversation)
            new_conversation.set_attribute(title="Tăng huyết áp" , create_date=datetime.now() , id_user=id_user)
            new_conversation.set_ID(id)
            session.add(new_conversation)

            new_message = Message()
            new_message.set_attribute(human=human_message , ai=ai_message , create_date=datetime.now() ,id_conversation=new_conversation.id)
            session.add(new_message)
            session.commit()

        except IntegrityError as e:
            session.rollback()
            error_message = "Error: {}".format(str(e))
            response = jsonify({"error": error_message})
            return response, 500

        response = jsonify({"msg": "Successfully"})
        return response, 200

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500


def check_message(id_user , id_message):
    message = EntityHandler.get_entity_id(session , Message , id_message)
    if message is None:
        return False
    else:
        conversation = EntityHandler.get_entity_id(session , Conversation , message.id_conversation)
        if conversation is None:
            return False
        if conversation.id_user == id_user:
            return True
        else:
            return False


@con_blueprint.route('/emotion', methods=["GET"])
@jwt_required()
# @limiter.limit("30 per minute")
def save_emotions():
    try:
        identity = get_jwt_identity()
        id_user = identity['id_user']
        id_message = int(request.args.get('id_message'))
        status = int(request.args.get('status'))

        if check_message(id_user , id_message):
            is_successfully = EntityHandler.update_status(session, Message, id_message, status)
            if is_successfully:
                response = jsonify({"msg": "Update status successfully"})
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












































