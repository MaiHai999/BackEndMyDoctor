from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from BackEnd.source.services.UserService import UserEntity
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:01692032691@localhost/MyDoctor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UserEn = UserEntity(db)
User = UserEn.create_model()



@app.route('/login', methods=['GET'] )
@cross_origin(origin='*')
def detectURL():
    users = user1.query.all()

    for user in users:
        print(f"ID: {user.id} , Email: {user.email}")

    result = "helo"
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5555')