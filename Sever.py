from flask import Flask
from BackEnd.source.controller.AccountController import auth_blueprint
from BackEnd.source.entity.MyConnectPro import MyConnectPro
from BackEnd.source.services.BlockTokenService import BlockToken

import Config
from datetime import timedelta
import os
from flask_jwt_extended import JWTManager
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/auth')

app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

# Route mặc định
@app.route('/')
def index():
    return 'Trang chủ'

#xem token có trong black list không
@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    user = os.environ.get('user_login')
    password_db = os.environ.get('password_login')
    db_manager = MyConnectPro(user, password_db)
    db_manager.connect()
    session = db_manager.get_session()
    jti = jwt_data['jti']
    token = session.query(BlockToken).filter(BlockToken.jti == jti).scalar()
    return token is not None


if __name__ == '__main__':
    app.run(debug=True)