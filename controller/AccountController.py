from flask import Flask
from flask_cors import CORS, cross_origin
from BackEnd.source.services.UserService import UserService
from BackEnd.source.entity.MyCustomApp import MyCustomApp

app_config = MyCustomApp()
app_config.connect_database("root" , "01692032691")
db = app_config.get_model()
app = app_config.get_app()

UserEntity = UserService(db)
User = UserEntity.create_model()

@app.route('/login', methods=['GET'] )
@cross_origin(origin='*')
def detectURL():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id} , Email: {user.email}")

    result = "helo"
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5555')