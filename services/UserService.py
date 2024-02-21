

class UserService:
    def __init__(self , db):
        self.db = db

    def create_model(self):
        class User(self.db.Model):
            __tablename__ = 'User'
            id = self.db.Column("ID", self.db.Integer, primary_key=True)
            email = self.db.Column('EMAIL', self.db.String(120), unique=False, nullable=True)
            password = self.db.Column('PASSWORD', self.db.String(30), nullable=True)
            id_facebook = self.db.Column('IDFACEBOOK', self.db.String(150), nullable=True)
            id_google = self.db.Column('IDGOOGLE', self.db.String(150), nullable=True)

        return User




