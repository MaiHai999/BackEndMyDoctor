import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"])

os.environ["user_login"] = 'root'
os.environ["password_login"] = '01692032691'
os.environ["tk_user"] = 'root'
os.environ["password_tk_user"] = '01692032691'
os.environ["SECRET_KEY"] = 'haideptrai'
os.environ["base_url"] = "http://192.168.1.2:9999/v1"
os.environ["path_vector_db"] = "/Users/maihai/PycharmProjects/MyDoctorPlus/BackEnd/asset/database/db_vector_en"
