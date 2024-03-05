from BackEnd.source.entity.MyConnectPro import MyConnectPro
from BackEnd.source.services.models import *
from BackEnd.source.entity.MyConnectPro import EntityHandler
from BackEnd.source.Config import limiter

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import NoResultFound

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol

import google.auth.transport.requests
import requests
import os

auth_blueprint = Blueprint('auth', __name__)

#tạo flow để đăng thực hiện liên kết với google
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
client_secrets_file = os.environ.get("client_secrets_file")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:3000/callback"
)






# Đăng nhập vào MySQL
user = os.environ.get('user_login')
password_db = os.environ.get('password_login')
db_manager = MyConnectPro(user, password_db)
db_manager.connect()
session_db = db_manager.get_session()


def check_login(email , password):
    try:
        user = session_db.query(User).filter(User.email == email).one()
        if check_password_hash(user.password , password):
            return user
        else:
            return False
    except NoResultFound:
        return None

@auth_blueprint.route('/login' , methods=['POST'])
@limiter.limit("20 per day")
def login():
    try:
        #Lấy các tham số
        email = request.json.get('email')
        password = request.json.get('password')
        user = check_login(email , password)

        #tạo tokens
        if user is None:
            return jsonify({"msg": "Email not registered"}), 401
        elif user is False:
            return jsonify({"msg": "Incorrect password"}), 401
        else:
            iden_info = {
                "id_user": user.id
            }

            access_token = create_access_token(identity=iden_info, fresh=True)
            refresh_token = create_refresh_token(identity=iden_info)
            return jsonify(user_name = user.email ,access_token=access_token, refresh_token=refresh_token) , 200

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

@auth_blueprint.route("/refresh_access", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access():
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        identity = get_jwt_identity()
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(refresh_token=refresh_token)
    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

@auth_blueprint.route('/logout', methods=["GET"])
@jwt_required()
@limiter.limit("20 per day")
def logout():
    try:
        jwt = get_jwt()
        jti = jwt['jti']
        token = BlockToken()
        token.set_attribute(jti)
        is_successfully = EntityHandler.save(session_db, token)
        if is_successfully:
            response = jsonify({"msg": "Logged out successfully"})
            return response, 200
        else:
            response = jsonify({"error": "Internal Server Error"})
            return response, 500



    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

def validation_register(email):
    try:
        user = session_db.query(User).filter(User.email == email).one()
        return 1
    except NoResultFound:
        return 0

@auth_blueprint.route('/register', methods=["POST"])
@limiter.limit("20 per day")
def register():
    try:
        #lấy các tham số
        email = request.json.get('email')
        password = request.json.get('password')

        if validation_register(email):
            response = jsonify({"msg": "Email already exists"})
            return response, 200
        else:
            users = User()
            users.set_attribute(email, password, None, None)
            is_successfully = EntityHandler.save(session_db, users)
            if is_successfully:
                response = jsonify({"msg": "Register successfully"})
                return response, 200
            else:
                response = jsonify({"error": "Internal Server Error"})
                return response, 500


    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500


@auth_blueprint.route('/login_gg' , methods=['post'])
def login_gg():
    try:
        authorization_url, state = flow.authorization_url()
        token = BlockToken()
        token.set_state(state)

        is_successfully = EntityHandler.save(session_db, token)
        if is_successfully:
            return jsonify({'authorization_url': authorization_url})
        else:
            response = jsonify({"error": "Internal Server Error"})
            return response, 500

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

def check_state(state):
    list_token = EntityHandler.get_all(session_db , BlockToken)
    for token in list_token:
        if token.state == state:
            is_successfully = EntityHandler.delete_entity(session_db , BlockToken , token.id)
            if is_successfully:
                return True
            else:
                return False

    return False

def check_google_id(google_id ):
    list_user = EntityHandler.get_all(session_db , User)
    for user in list_user:
        if user.id_google == google_id:
            return user

    return None
def check_email(email):
    list_user = EntityHandler.get_all(session_db, User)
    for user in list_user:
        if user.email == email:
            return True

    return False

@auth_blueprint.route("/callback")
def callback():
    try:
        flow.fetch_token(authorization_response=request.url)
        result = check_state(request.args["state"])

        if result is False:
            response = jsonify({"error": "User not authenticated"})
            return response, 403

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        google_id = id_info.get("sub")
        name = id_info.get("name")
        email = id_info.get("email")

        user = check_google_id(google_id)

        if user is not None:
            iden_info = {
                "id_user": user.id
            }
            access_token = create_access_token(identity=iden_info, fresh=True)
            refresh_token = create_refresh_token(identity=iden_info)
            return jsonify(user_name=name, access_token=access_token, refresh_token=refresh_token), 200
        else:
            is_email = check_email(email)
            if is_email:
                response = jsonify({"error": "Email already exists"})
                return response, 500
            else:
                users = User()
                users.set_attribute(email, None, None, google_id)
                is_successfully = EntityHandler.save(session_db, users)
                if is_successfully:

                    iden_info = {
                        "id_user": users.id
                    }
                    access_token = create_access_token(identity=iden_info, fresh=True)
                    refresh_token = create_refresh_token(identity=iden_info)
                    return jsonify(user_name=name, access_token=access_token, refresh_token=refresh_token), 200
                else:
                    response = jsonify({"error": "Internal Server Error"})
                    return response, 500


    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500


















