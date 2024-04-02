import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail


limiter = Limiter(get_remote_address, default_limits=["900 per day", "300 per hour"])
mail = Mail()


current_directory = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(current_directory, 'BackEnd')):
    current_directory = os.path.dirname(current_directory)

project_root = current_directory


os.environ["user_login"] = 'root'
os.environ["password_login"] = '01692032691'

os.environ["tk_user"] = 'root'
os.environ["password_tk_user"] = '01692032691'

os.environ["SECRET_KEY_JWT"] = 'haideptrai'
os.environ["base_url"] = "http://192.168.1.5:9999/v1"

os.environ["path_vector_db"] = project_root + "/BackEnd/asset/database/db_vector_en"

os.environ["client_secrets_file"] = project_root + "/BackEnd/asset/client_secret.json"
os.environ["GOOGLE_CLIENT_ID"] = "309708343797-apbnss2jt41pb0jo3baj1d5bjjpbj71f.apps.googleusercontent.com"

os.environ["SECRET_KEY"] = "ongbagiataolohet"
os.environ["SECURITY_PASSWORD_SALT"] = "fkslkfsdlkfrgufnsfd"

os.environ["MAIL_USERNAME"] = "maithanhhai.tt@gmail.com"
os.environ["MAIL_PASSWORD"] = "govnerbainslqhaj"
