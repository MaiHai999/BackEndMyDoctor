import Config
from BackEnd.source.Config import limiter
from flask import Flask
from BackEnd.source.controller.AccountController import auth_blueprint
from BackEnd.source.controller.ConversationController import con_blueprint
from BackEnd.source.entity.MyConnectPro import MyConnectPro
from BackEnd.source.services.models import *
from datetime import timedelta
import os
from flask_jwt_extended import JWTManager
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(con_blueprint, url_prefix='/mess')

app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)
limiter.init_app(app)


#xem token có trong black list không
@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    try:
        user = os.environ.get('user_login')
        password_db = os.environ.get('password_login')
        db_manager = MyConnectPro(user, password_db)
        db_manager.connect()
        session = db_manager.get_session()
        jti = jwt_data['jti']
        token = session.query(BlockToken).filter(BlockToken.jti == jti).scalar()
        return token is not None

    except Exception as e:
        error_message = "Error: {}".format(str(e))
        response = jsonify({"error": error_message})
        return response, 500



if __name__ == '__main__':
    app.run(debug=True)