

from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

class TokenVertification:

    @staticmethod
    def generate_token(email , password):
        data = {"email": email, "password": password}
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        return serializer.dumps(data, salt=SECURITY_PASSWORD_SALT)

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        try:
            data = serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=expiration)
            return data
        except Exception:
            return False




