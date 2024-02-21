


class TokenService:
    def __init__(self , db):
        self.db = db

    def create_model(self):
        class Token(self.db.Model):
            __tablename__ = 'Tokens'
            id = self.db.Column("ID", self.db.Integer, primary_key=True)
            access_token = self.db.Column('ACCESS_TOKEN', self.db.String(255), unique=True, nullable=False)
            expiration_access = self.db.Column('EXPIRATION_ACCESS', self.db.DateTime, unique=False, nullable=False)
            refresh_token = self.db.Column('REFRESH_TOKEN', self.db.String(255), unique=True, nullable=False)
            expiration_refresh = self.db.Column('EXPIRATION_REFRESH', self.db.DateTime, unique=False, nullable=False)
            id_user = self.db.Column('IDUSER', self.db.Integer, nullable=True)

        return Token

