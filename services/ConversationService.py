

class ConversationService:
    def __init__(self, db):
        self.db = db

    def create_models(self):
        class Conversation(self.db.Model):
            __tablename__ = 'Conversations'
            id = self.db.Column("ID", self.db.Integer, primary_key=True)
            title = self.db.Column('TITLE', self.db.String(300), unique=False, nullable=True)
            create_date = self.db.Column('CREATDATE', self.db.DateTime, nullable=True)
            id_user = self.db.Column('IDUSER', self.db.Integer, nullable=True)
            status = self.db.Column('STATUS', self.db.Integer, nullable=True)

        return Conversation