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
from flask import jsonify
import os

auth_blueprint = Blueprint('auth', __name__)


# Đăng nhập vào MySQL
user = os.environ.get('user_login')
password_db = os.environ.get('password_login')
db_manager = MyConnectPro(user, password_db)
db_manager.connect()
session = db_manager.get_session()


def check_login(email , password):
    try:
        user = session.query(User).filter(User.email == email).one()
        return check_password_hash(user.password , password), user
    except NoResultFound:
        return 0 , 0

@auth_blueprint.route('/login' , methods=['POST'])
def login():
    try:
        #Lấy các tham số
        email = request.json.get('email')
        password = request.json.get('password')
        role , user = check_login(email , password)

        #tạo tokens
        if role:
            role_info = {
                "role": user.role,
                "id_user": user.id
            }

            access_token = create_access_token(identity=role_info, fresh=True)
            refresh_token = create_refresh_token(identity=role_info)
            return jsonify(user_name = user.email ,access_token=access_token, refresh_token=refresh_token) , 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401

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
def logout():
    try:
        jwt = get_jwt()
        jti = jwt['jti']
        token = BlockToken()
        token.set_attribute(jti)
        EntityHandler.save(session, token)
        response = jsonify({"msg": "Logged out successfully"})
        return response, 200

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500

def validation_register(email):
    try:
        user = session.query(User).filter(User.email == email).one()
        return 1
    except NoResultFound:
        return 0

@auth_blueprint.route('/register', methods=["POST"])
def register():
    try:
        #lấy các tham số
        email = request.json.get('email')
        password = request.json.get('password')
        role = request.json.get('role')

        if validation_register(email):
            response = jsonify({"msg": "Email already exists"})
            return response, 200
        else:
            users = User()
            users.set_attribute(email, password, None, None, role)
            EntityHandler.save(session, users)
            response = jsonify({"msg": "Register successfully"})
            return response , 200

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500


@auth_blueprint.route('/test', methods=["GET"])
@jwt_required()
def protect():
    response = jsonify({"msg": "test"})
    return response, 200

